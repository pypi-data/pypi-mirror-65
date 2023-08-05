import re
import logging

import pypeg2
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QCoreApplication, QLocale, QDateTime
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QMessageBox

from duniterpy.constants import PUBKEY_REGEX
from duniterpy.documents import CRCPubkey
from duniterpy.grammars.output import Condition

from sakia.data.processors import ConnectionsProcessor
from sakia.decorators import asyncify
from sakia.gui.sub.password_input import PasswordInputController
from sakia.gui.sub.search_user.controller import SearchUserController
from sakia.gui.sub.user_information.controller import UserInformationController
from sakia.money import Quantitative
from sakia.gui.widgets.dialogs import dialog_async_exec
from sakia.services import sources
from .model import TransferModel
from .view import TransferView


class TransferController(QObject):
    """
    The transfer component controller
    """

    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, view, model, search_user, user_information, password_input):
        """
        Constructor of the transfer component

        :param sakia.gui.dialogs.transfer.view.TransferView: the view
        :param sakia.gui.dialogs.transfer.model.TransferModel model: the model
        """
        super().__init__()
        self.view = view
        self.model = model  # type: TransferModel
        self.search_user = search_user
        self.user_information = user_information
        self.password_input = password_input
        self.password_input.set_info_visible(False)
        self.password_input.password_changed.connect(self.refresh)
        self.view.button_box.accepted.connect(self.accept)
        self.view.button_box.rejected.connect(self.reject)
        self.view.radio_pubkey.toggled.connect(self.refresh)
        self.view.edit_pubkey.textChanged.connect(self.refresh)
        self.view.combo_connections.currentIndexChanged.connect(
            self.change_current_connection
        )
        self.view.spinbox_amount.valueChanged.connect(self.handle_amount_change)
        self.view.spinbox_relative.valueChanged.connect(self.handle_relative_change)
        self.view.button_source_check.clicked.connect(self.check_source_dialog)

    @classmethod
    def create(cls, parent, app):
        """
        Instanciate a transfer component
        :param sakia.gui.component.controller.ComponentController parent:
        :param sakia.app.Application app:
        :return: a new Transfer controller
        :rtype: TransferController
        """
        search_user = SearchUserController.create(None, app)
        user_information = UserInformationController.create(None, app, None)
        password_input = PasswordInputController.create(None, None)

        view = TransferView(
            parent.view if parent else None,
            search_user.view,
            user_information.view,
            password_input.view,
        )
        model = TransferModel(app)
        controller = cls(view, model, search_user, user_information, password_input)

        search_user.identity_selected.connect(user_information.search_identity)

        view.set_keys(controller.model.available_connections())
        view.set_contacts(controller.model.contacts())
        app.new_connection.connect(view.add_key)
        app.connection_removed.connect(view.remove_key)

        return controller

    @classmethod
    def integrate_to_main_view(cls, parent, app, connection):
        controller = cls.create(parent, app)
        controller.view.combo_connections.setCurrentText(connection.title())
        controller.view.radio_pubkey.toggle()
        controller.view.widget_connections.hide()
        controller.view.widget_source.hide()
        controller.view.label_total.hide()
        return controller

    @classmethod
    def open_transfer_with_pubkey(cls, parent, app, connection, pubkey, source):
        controller = cls.create(parent, app)
        controller.view.widget_connections.show()
        if connection:
            controller.view.combo_connections.setCurrentText(connection.title())
        if pubkey:
            controller.view.edit_pubkey.setText(pubkey)
            controller.view.radio_pubkey.setChecked(True)
            controller.view.radio_pubkey.toggle()
        else:
            controller.view.radio_local_key.setChecked(True)
            controller.view.radio_local_key.toggle()
        if source:
            controller.model.current_source = source
            controller.view.label_source_identifier.setText(
                "{}:{}".format(source.identifier, source.noffset)
            )
            controller.set_amount_value(source.amount, source.base)
            controller.view.spinbox_amount.setDisabled(True)
            controller.view.spinbox_relative.setDisabled(True)
            result, _ = controller.check_source(source)
            # by default, source is unlocked, if not...
            if not result:
                # enabled the check button to open the errors dialog
                controller.view.button_source_check.setEnabled(True)
        else:
            controller.view.widget_source.hide()

        controller.refresh()
        return controller

    @classmethod
    def send_money_to_pubkey(cls, parent, app, connection, pubkey, source):
        dialog = QDialog(parent)
        dialog.setWindowTitle(
            QCoreApplication.translate("TransferController", "Transfer")
        )
        dialog.setLayout(QVBoxLayout(dialog))
        controller = cls.open_transfer_with_pubkey(
            parent, app, connection, pubkey, source
        )

        dialog.layout().addWidget(controller.view)
        controller.accepted.connect(dialog.accept)
        controller.rejected.connect(dialog.reject)
        return dialog.exec()

    @classmethod
    def send_money_to_identity(cls, parent, app, connection, identity):
        dialog = QDialog(parent)
        dialog.setWindowTitle(
            QCoreApplication.translate("TransferController", "Transfer")
        )
        dialog.setLayout(QVBoxLayout(dialog))
        controller = cls.open_transfer_with_pubkey(
            parent, app, connection, identity.pubkey, None
        )

        controller.user_information.change_identity(identity)
        dialog.layout().addWidget(controller.view)
        controller.accepted.connect(dialog.accept)
        controller.rejected.connect(dialog.reject)
        return dialog.exec()

    @classmethod
    def send_transfer_again(cls, parent, app, connection, resent_transfer):
        dialog = QDialog(parent)
        dialog.setWindowTitle(
            QCoreApplication.translate("TransferController", "Transfer")
        )
        dialog.setLayout(QVBoxLayout(dialog))
        controller = cls.create(parent, app)
        controller.view.widget_connections.show()
        controller.view.label_total.show()
        controller.view.combo_connections.setCurrentText(connection.title())
        controller.view.edit_pubkey.setText(resent_transfer.receivers[0])
        controller.view.radio_pubkey.setChecked(True)

        controller.refresh()

        # display transaction amount
        controller.set_amount_value(resent_transfer.amount, resent_transfer.amount_base)

        connections_processor = ConnectionsProcessor.instanciate(app)
        wallet_index = connections_processor.connections().index(connection)
        controller.view.combo_connections.setCurrentIndex(wallet_index)
        controller.view.edit_pubkey.setText(resent_transfer.receivers[0])
        controller.view.radio_pubkey.toggle()
        controller.view.edit_message.setText(resent_transfer.comment)
        dialog.layout().addWidget(controller.view)
        controller.accepted.connect(dialog.accept)
        controller.rejected.connect(dialog.reject)
        return dialog.exec()

    def valid_crc_pubkey(self):
        if self.view.pubkey_value():
            try:
                crc_pubkey = CRCPubkey.from_pubkey(self.view.pubkey_value())
                return crc_pubkey.is_valid()
            except AttributeError:
                return False
        else:
            return False

    def selected_pubkey(self):
        """
        Get selected pubkey in the widgets of the window
        :return: the current pubkey
        :rtype: str
        """
        pubkey = None

        if self.view.recipient_mode() == TransferView.RecipientMode.SEARCH:
            if self.search_user.current_identity():
                pubkey = self.search_user.current_identity().pubkey
        elif self.view.recipient_mode() == TransferView.RecipientMode.LOCAL_KEY:
            pubkey = self.model.connection_pubkey(self.view.local_key_selected())
        elif self.view.recipient_mode() == TransferView.RecipientMode.CONTACT:
            index = self.view.contact_selected()
            if index >= 0:
                pubkey = self.model.contacts()[index].pubkey
        elif self.view.pubkey_value():
            try:
                crc_pubkey = CRCPubkey.from_pubkey(self.view.pubkey_value())
                if crc_pubkey.is_valid():
                    pubkey = crc_pubkey.pubkey
            except AttributeError:
                result = re.compile("^({0})$".format(PUBKEY_REGEX)).match(
                    self.view.pubkey_value()
                )
                if result:
                    pubkey = self.view.pubkey_value()
        return pubkey

    @asyncify
    async def accept(self):
        logging.debug("Accept transfer action...")
        self.view.button_box.setEnabled(False)

        source = self.model.current_source

        logging.debug("checking recipient mode...")
        recipient = self.selected_pubkey()
        amount = self.view.spinbox_amount.value() * 100
        amount_base = self.model.current_base()

        logging.debug("Showing password dialog...")
        secret_key, password = self.password_input.get_salt_password()

        logging.debug("Setting cursor...")
        QApplication.setOverrideCursor(Qt.WaitCursor)

        comment = self.view.edit_message.text()
        lock_mode = self.view.combo_locks.currentIndex()

        logging.debug("Send money...")
        result, transactions = await self.model.send_money(
            recipient,
            secret_key,
            password,
            amount,
            amount_base,
            comment,
            lock_mode,
            source,
        )
        if result[0]:
            await self.view.show_success(self.model.notifications(), recipient)
            logging.debug("Restore cursor...")
            QApplication.restoreOverrideCursor()
            self.view.button_box.setEnabled(True)

            # If we sent back a transaction we cancel the first one
            self.model.cancel_previous()
            for tx in transactions:
                self.model.app.new_transfer.emit(self.model.connection, tx)
            self.view.clear()
            self.rejected.emit()
        else:
            await self.view.show_error(self.model.notifications(), result[1])
            for tx in transactions:
                self.model.app.new_transfer.emit(self.model.connection, tx)

            QApplication.restoreOverrideCursor()
            self.view.button_box.setEnabled(True)

    def reject(self):
        self.view.clear()
        self.rejected.emit()

    def refresh(self):
        amount = self.model.wallet_value()
        current_base = self.model.current_base()
        current_base_amount = amount / pow(10, current_base)
        total_text = self.model.localized_amount(amount)
        self.view.refresh_labels(total_text)

        if amount == 0:
            self.view.set_button_box(TransferView.ButtonBoxState.NO_AMOUNT)
        if not self.selected_pubkey():
            if self.view.pubkey_value() and not self.valid_crc_pubkey():
                self.view.set_button_box(TransferView.ButtonBoxState.WRONG_RECIPIENT)
            else:
                self.view.set_button_box(TransferView.ButtonBoxState.NO_RECEIVER)
        elif self.password_input.valid():
            # if source and check source successful...
            self.view.set_button_box(TransferView.ButtonBoxState.OK)
        else:
            self.view.set_button_box(TransferView.ButtonBoxState.WRONG_PASSWORD)
        # if source and check source button still enabled...
        if self.model.current_source and self.view.button_source_check.isEnabled():
            self.view.set_button_box(TransferView.ButtonBoxState.SOURCE_LOCKED)

        max_relative = self.model.quant_to_rel(current_base_amount / 100)
        self.view.spinbox_amount.setSuffix(Quantitative.base_str(current_base))

        self.view.set_spinboxes_parameters(current_base_amount / 100, max_relative)

    def handle_amount_change(self, value):
        relative = self.model.quant_to_rel(value)
        self.view.change_relative_amount(relative)
        self.refresh()

    def handle_relative_change(self, value):
        amount = self.model.rel_to_quant(value)
        self.view.change_quantitative_amount(amount)
        self.refresh()

    def change_current_connection(self, index):
        self.model.set_connection(index)
        self.password_input.set_connection(self.model.connection)
        self.refresh()

    def check_source(self, source):
        """
        Check source conditions lock status

        Return a tupple with :
            result: bool,
            errors: list of tuples
                [(condition: str, message: str, info: int|str),...]

        :param source:
        :return tuple:
        """
        # evaluate condition
        condition = pypeg2.parse(source.conditions, Condition)
        result, _errors = self.model.app.sources_service.evaluate_condition(
            self.model.app.currency,
            condition,
            [self.model.connection.pubkey],
            [],
            source.identifier,
        )
        return result, _errors

    def check_source_dialog(self):
        """
        Open check source result and errors dialog

        :return:
        """
        source = self.model.current_source
        result, _errors = self.check_source(source)

        # if success...
        if result:
            message = QCoreApplication.translate(
                "TransferController", "Check is successful!"
            )
            self.view.button_source_check.setDisabled(True)
            self.refresh()
        # if failure...
        else:
            message = QCoreApplication.translate(
                "TransferController", "<p><b>Condition</b></p>{}"
            ).format(source.conditions)
            message += QCoreApplication.translate(
                "TransferController", "<p><b>Errors</b><p>"
            )
            message += "<ul>"
            # add error messages
            for (_condition, _error, _param) in _errors:
                if isinstance(_param, int):
                    _param = (
                        QLocale.toString(
                            QLocale(),
                            QDateTime.fromTime_t(_param),
                            QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
                        )
                        + " BAT"
                    )
                message += QCoreApplication.translate(
                    "TransferController",
                    '<li>Error in {}: <span style="color: red">{} {}</span></li>',
                ).format(
                    _condition,
                    QCoreApplication.translate("SourcesServices", _error),
                    _param,
                )
            message += "</ul>"
        # open message box displaying source check result
        qmessagebox = QMessageBox(self.view)
        qmessagebox.setWindowTitle(
            QCoreApplication.translate("TransferController", "Check source condition")
        )
        qmessagebox.setText(message)
        qmessagebox.exec()

    def set_amount_value(self, amount, base):
        """
        Set quantitative and relative amounts from amount and base given
        :param int amount: Amount to display
        :param int base: Base of the amount given
        :return:
        """
        # calculate amount for current base
        current_base = self.model.current_base()
        current_base_amount = amount / pow(10, base - current_base)
        # display quantitative and relative amounts
        relative = self.model.quant_to_rel(current_base_amount / 100)
        self.view.set_spinboxes_parameters(current_base_amount / 100, relative)
        self.view.change_relative_amount(relative)
        self.view.change_quantitative_amount(current_base_amount / 100)
