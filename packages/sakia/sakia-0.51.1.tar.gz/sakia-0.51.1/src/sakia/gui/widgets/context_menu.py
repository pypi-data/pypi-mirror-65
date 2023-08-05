import logging
import re
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QMenu, QAction, QApplication, QMessageBox

from duniterpy.constants import PUBKEY_REGEX
from duniterpy.documents.crc_pubkey import CRCPubkey
from duniterpy.grammars.output import Condition, SIG

from sakia.app import Application
from sakia.data.entities import Identity, Transaction, Dividend, Connection, Source
from sakia.data.processors import BlockchainProcessor, TransactionsProcessor
from sakia.decorators import asyncify
from sakia.gui.sub.certification.controller import CertificationController
from sakia.gui.sub.transfer.controller import TransferController
from sakia.gui.sub.user_information.controller import UserInformationController


class ContextMenu(QObject):
    view_identity_in_wot = pyqtSignal(object)
    identity_information_loaded = pyqtSignal(Identity)

    def __init__(self, qmenu: QMenu, app: Application, connection: Connection):
        """
        :param PyQt5.QtWidgets.QMenu: the qmenu widget
        :param sakia.app.Application app: Application instance
        :param sakia.data.entities.Connection connection: The current connection instance
        """
        super().__init__()
        self.qmenu = qmenu
        self._app = app  # type: Application
        self._connection = connection

    @staticmethod
    def _add_identity_actions(menu, identity):
        """
        :param ContextMenu menu: the qmenu to add actions to
        :param Identity identity: the identity
        """
        menu.qmenu.addSeparator().setText(
            identity.uid if identity.uid else identity.pubkey[:7]
        )

        informations = QAction(
            QCoreApplication.translate("ContextMenu", "Informations"),
            menu.qmenu.parent(),
        )
        informations.triggered.connect(lambda checked, i=identity: menu.informations(i))
        menu.qmenu.addAction(informations)

        if identity.uid and (
            not menu._connection or menu._connection.pubkey != identity.pubkey
        ):
            certify = QAction(
                QCoreApplication.translate("ContextMenu", "Certify identity"),
                menu.qmenu.parent(),
            )
            certify.triggered.connect(
                lambda checked, i=identity: menu.certify_identity(i)
            )
            menu.qmenu.addAction(certify)

            view_wot = QAction(
                QCoreApplication.translate("ContextMenu", "View in Web of Trust"),
                menu.qmenu.parent(),
            )
            view_wot.triggered.connect(lambda checked, i=identity: menu.view_wot(i))
            menu.qmenu.addAction(view_wot)

            send_money = QAction(
                QCoreApplication.translate("ContextMenu", "Send money"),
                menu.qmenu.parent(),
            )
            send_money.triggered.connect(lambda checked, i=identity: menu.send_money(i))
            menu.qmenu.addAction(send_money)

        copy_pubkey = QAction(
            QCoreApplication.translate("ContextMenu", "Copy pubkey to clipboard"),
            menu.qmenu.parent(),
        )
        copy_pubkey.triggered.connect(
            lambda checked, i=identity: ContextMenu.copy_pubkey_to_clipboard(i)
        )
        menu.qmenu.addAction(copy_pubkey)

        copy_pubkey = QAction(
            QCoreApplication.translate(
                "ContextMenu", "Copy pubkey to clipboard (with CRC)"
            ),
            menu.qmenu.parent(),
        )
        copy_pubkey.triggered.connect(
            lambda checked, i=identity: ContextMenu.copy_pubkey_to_clipboard_with_crc(i)
        )
        menu.qmenu.addAction(copy_pubkey)

        if identity.uid and menu._app.parameters.expert_mode:
            copy_selfcert = QAction(
                QCoreApplication.translate(
                    "ContextMenu", "Copy self-certification document to clipboard"
                ),
                menu.qmenu.parent(),
            )
            copy_selfcert.triggered.connect(
                lambda checked, i=identity: menu.copy_selfcert_to_clipboard(i)
            )
            menu.qmenu.addAction(copy_selfcert)

    @staticmethod
    def _add_transfer_actions(menu, transfer: Transaction):
        """
        :param ContextMenu menu: the qmenu to add actions to
        :param Transfer transfer: the transfer
        """
        menu.qmenu.addSeparator().setText(
            QCoreApplication.translate("ContextMenu", "Transfer")
        )
        if transfer.state in (Transaction.REFUSED, Transaction.TO_SEND):
            send_back = QAction(
                QCoreApplication.translate("ContextMenu", "Send again"),
                menu.qmenu.parent(),
            )
            send_back.triggered.connect(
                lambda checked, tr=transfer: menu.send_again(tr)
            )
            menu.qmenu.addAction(send_back)

            cancel = QAction(
                QCoreApplication.translate("ContextMenu", "Cancel"), menu.qmenu.parent()
            )
            cancel.triggered.connect(
                lambda checked, tr=transfer: menu.cancel_transfer(tr)
            )
            menu.qmenu.addAction(cancel)

        # if special lock condition on transaction or
        # all transaction received in expert mode...
        if transfer.conditions is not None or (
            transfer.pubkey in transfer.receivers and menu._app.parameters.expert_mode
        ):
            conditions = (
                transfer.conditions
                if transfer.conditions
                else Condition.token(SIG.token(transfer.pubkey)).compose(Condition())
            )
            # get source from transfer infos
            source = menu._app.sources_service.get_one(
                currency=transfer.currency,
                identifier=transfer.sha_hash,
                conditions=conditions,
                type=Source.TYPE_TRANSACTION,
                pubkey=menu._connection.pubkey,
            )
            if source:
                # add send as source menu
                send_as_source = QAction(
                    QCoreApplication.translate("ContextMenu", "Send as source"),
                    menu.qmenu.parent(),
                )
                send_as_source.triggered.connect(
                    lambda checked, src=source: menu.send_as_source(src)
                )
                menu.qmenu.addAction(send_as_source)

        if menu._app.parameters.expert_mode:
            copy_doc = QAction(
                QCoreApplication.translate(
                    "ContextMenu", "Copy raw transaction to clipboard"
                ),
                menu.qmenu.parent(),
            )
            copy_doc.triggered.connect(
                lambda checked, tx=transfer: menu.copy_transaction_to_clipboard(tx)
            )
            menu.qmenu.addAction(copy_doc)

            if transfer.blockstamp:
                copy_doc = QAction(
                    QCoreApplication.translate(
                        "ContextMenu", "Copy transaction block to clipboard"
                    ),
                    menu.qmenu.parent(),
                )
                copy_doc.triggered.connect(
                    lambda checked, number=transfer.blockstamp.number: menu.copy_block_to_clipboard(
                        transfer.blockstamp.number
                    )
                )
                menu.qmenu.addAction(copy_doc)

    @staticmethod
    def _add_dividend_actions(menu, dividend):
        """
        :param ContextMenu menu: the qmenu to add actions to
        :param Transfer transfer: the transfer
        """
        menu.qmenu.addSeparator().setText(
            QCoreApplication.translate("ContextMenu", "Dividend")
        )

        if menu._app.parameters.expert_mode:
            # get dividend source from block number and type
            source = menu._app.sources_service.get_one(
                noffset=dividend.block_number,
                type=Source.TYPE_DIVIDEND,
                pubkey=menu._connection.pubkey,
            )
            if source:
                # add send as source menu
                send_as_source = QAction(
                    QCoreApplication.translate("ContextMenu", "Send as source"),
                    menu.qmenu.parent(),
                )
                send_as_source.triggered.connect(
                    lambda checked, src=source: menu.send_dividend_as_source(src)
                )
                menu.qmenu.addAction(send_as_source)

    @staticmethod
    def _add_string_actions(menu, str_value):
        if re.match(PUBKEY_REGEX, str_value):
            menu.qmenu.addSeparator().setText(str_value[:7])
            copy_pubkey = QAction(
                QCoreApplication.translate("ContextMenu", "Copy pubkey to clipboard"),
                menu.qmenu.parent(),
            )
            copy_pubkey.triggered.connect(
                lambda checked, p=str_value: ContextMenu.copy_pubkey_to_clipboard(p)
            )
            menu.qmenu.addAction(copy_pubkey)

            copy_pubkey = QAction(
                QCoreApplication.translate(
                    "ContextMenu", "Copy pubkey to clipboard (with CRC)"
                ),
                menu.qmenu.parent(),
            )
            copy_pubkey.triggered.connect(
                lambda checked, p=str_value: ContextMenu.copy_pubkey_to_clipboard_with_crc(
                    p
                )
            )
            menu.qmenu.addAction(copy_pubkey)

            if menu._connection.pubkey != str_value:
                send_money = QAction(
                    QCoreApplication.translate("ContextMenu", "Send money"),
                    menu.qmenu.parent(),
                )
                send_money.triggered.connect(
                    lambda checked, p=str_value: menu.send_money(p)
                )
                menu.qmenu.addAction(send_money)

    @classmethod
    def from_data(cls, parent, app, connection, data):
        """
        Builds a QMenu from data passed as parameters
        Data can be Identity or Transfer

        :param PyQt5.QtWidgets.QWidget parent: the parent widget
        :param sakia.app.Application app: Application instance
        :param sakia.data.entities.Connection connection: the current connection
        :param tuple data: a tuple of data to add to the menu
        :rtype: ContextMenu
        """
        menu = cls(QMenu(parent), app, connection)
        build_actions = {
            Identity: ContextMenu._add_identity_actions,
            Transaction: ContextMenu._add_transfer_actions,
            Dividend: ContextMenu._add_dividend_actions,
            str: ContextMenu._add_string_actions,
            dict: lambda m, d: None,
            type(None): lambda m, d: None,
        }
        for d in data:
            build_actions[type(d)](menu, d)

        return menu

    @staticmethod
    def copy_pubkey_to_clipboard(identity_or_pubkey):
        clipboard = QApplication.clipboard()
        if isinstance(identity_or_pubkey, Identity):
            clipboard.setText(identity_or_pubkey.pubkey)
        else:
            clipboard.setText(identity_or_pubkey)

    @staticmethod
    def copy_pubkey_to_clipboard_with_crc(identity_or_pubkey):
        clipboard = QApplication.clipboard()
        if isinstance(identity_or_pubkey, Identity):
            clipboard.setText(str(CRCPubkey.from_pubkey(identity_or_pubkey.pubkey)))
        else:
            clipboard.setText(str(CRCPubkey.from_pubkey(identity_or_pubkey)))

    def informations(self, identity):
        if identity.uid:
            UserInformationController.show_identity(self.parent(), self._app, identity)
            self.identity_information_loaded.emit(identity)
        else:
            UserInformationController.search_and_show_pubkey(
                self.parent(), self._app, identity.pubkey
            )

    def send_money(self, identity_or_pubkey):
        if isinstance(identity_or_pubkey, Identity):
            TransferController.send_money_to_identity(
                None, self._app, self._connection, identity_or_pubkey
            )
        else:
            TransferController.send_money_to_pubkey(
                None, self._app, self._connection, identity_or_pubkey, None
            )

    def view_wot(self, identity):
        self.view_identity_in_wot.emit(identity)

    def certify_identity(self, identity):
        CertificationController.certify_identity(
            None, self._app, self._connection, identity
        )

    def send_again(self, transfer):
        TransferController.send_transfer_again(
            None, self._app, self._connection, transfer
        )

    def cancel_transfer(self, transfer):
        reply = QMessageBox.warning(
            self.qmenu,
            QCoreApplication.translate("ContextMenu", "Warning"),
            QCoreApplication.translate(
                "ContextMenu",
                """Are you sure?
This money transfer will be removed and not sent.""",
            ),
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if reply == QMessageBox.Ok:
            transactions_processor = TransactionsProcessor.instanciate(self._app)
            if transactions_processor.cancel(transfer):
                self._app.sources_service.restore_sources(
                    self._connection.pubkey, transfer
                )
            self._app.db.commit()
            self._app.transaction_state_changed.emit(transfer)

    def send_as_source(self, source: Source):
        """
        Open transfer dialog with a transaction as source

        :param Source source: Source entity to send
        :return:
        """
        TransferController.send_money_to_pubkey(
            None, self._app, self._connection, None, source
        )

    def send_dividend_as_source(self, source: Source):
        """
        Open transfer dialog with a dividend as source

        :param Source source: Source entity to send
        :return:
        """
        TransferController.send_money_to_pubkey(
            None, self._app, self._connection, None, source
        )

    def copy_transaction_to_clipboard(self, tx):
        clipboard = QApplication.clipboard()
        clipboard.setText(tx.raw)

    @asyncify
    async def copy_block_to_clipboard(self, number):
        clipboard = QApplication.clipboard()
        blockchain_processor = BlockchainProcessor.instanciate(self._app)
        block_doc = await blockchain_processor.get_block(
            self._connection.currency, number
        )
        clipboard.setText(block_doc.signed_raw())

    @asyncify
    async def copy_selfcert_to_clipboard(self, identity):
        """

        :param sakia.core.registry.Identity identity:
        :return:
        """
        clipboard = QApplication.clipboard()
        selfcert = await identity.selfcert(self._community)
        clipboard.setText(selfcert.signed_raw())
