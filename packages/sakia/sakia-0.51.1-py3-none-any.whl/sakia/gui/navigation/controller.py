from PyQt5.QtCore import pyqtSignal, QObject, Qt, QCoreApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox

from duniterpy.key import SigningKey
from sakia.data.entities import Connection
from sakia.decorators import asyncify
from sakia.gui.sub.password_input import PasswordInputController
from sakia.gui.widgets import toast
from sakia.gui.widgets.dialogs import (
    QAsyncMessageBox,
    dialog_async_exec,
    QAsyncFileDialog,
)
from sakia.models.generic_tree import GenericTreeModel
from .graphs.wot.controller import WotController
from .homescreen.controller import HomeScreenController
from .identities.controller import IdentitiesController
from .identity.controller import IdentityController
from .model import NavigationModel
from .network.controller import NetworkController
from .txhistory.controller import TxHistoryController
from .view import NavigationView


class NavigationController(QObject):
    """
    The navigation panel
    """

    currency_changed = pyqtSignal(str)
    connection_changed = pyqtSignal(Connection)

    def __init__(self, parent, view, model):
        """
        Constructor of the navigation component

        :param sakia.gui.navigation.view.NavigationView view: the view
        :param sakia.gui.navigation.model.NavigationModel model: the model
        """
        super().__init__(parent)
        self.view = view
        self.model = model
        self.components = {
            "TxHistory": TxHistoryController,
            "HomeScreen": HomeScreenController,
            "Network": NetworkController,
            "Identities": IdentitiesController,
            "Informations": IdentityController,
            "Wot": WotController,
        }
        self.view.current_view_changed.connect(self.handle_view_change)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.tree_context_menu)
        self._components_controllers = []

    @classmethod
    def create(cls, parent, app):
        """
        Instanciate a navigation component
        :param sakia.app.Application app: the application
        :return: a new Navigation controller
        :rtype: NavigationController
        """
        view = NavigationView(None)
        model = NavigationModel(None, app)
        navigation = cls(parent, view, model)
        model.setParent(navigation)
        navigation.init_navigation()
        app.new_connection.connect(navigation.add_connection)
        app.view_in_wot.connect(navigation.open_wot_view)
        app.identity_changed.connect(navigation.handle_identity_change)
        return navigation

    def open_network_view(self, _):
        raw_data = self.model.get_raw_data("Network")
        if raw_data:
            widget = raw_data["widget"]
            if self.view.stacked_widget.indexOf(widget) != -1:
                self.view.stacked_widget.setCurrentWidget(widget)
                self.view.current_view_changed.emit(raw_data)
                return

    def open_wot_view(self, _):
        raw_data = self.model.get_raw_data("Wot")
        if raw_data:
            widget = raw_data["widget"]
            if self.view.stacked_widget.indexOf(widget) != -1:
                self.view.stacked_widget.setCurrentWidget(widget)
                self.view.current_view_changed.emit(raw_data)
                return

    def open_identities_view(self, _):
        raw_data = self.model.get_raw_data("Identities")
        if raw_data:
            widget = raw_data["widget"]
            if self.view.stacked_widget.indexOf(widget) != -1:
                self.view.stacked_widget.setCurrentWidget(widget)
                self.view.current_view_changed.emit(raw_data)
                return

    def parse_node(self, node_data):
        if "component" in node_data:
            component_class = self.components[node_data["component"]]
            component = component_class.create(
                self, self.model.app, **node_data["dependencies"]
            )
            self._components_controllers.append(component)
            widget = self.view.add_widget(component.view)
            node_data["widget"] = widget
        if "children" in node_data:
            for child in node_data["children"]:
                self.parse_node(child)

    def init_navigation(self):
        self.model.init_navigation_data()

        for node in self.model.navigation:
            self.parse_node(node)

        self.view.set_model(self.model)

    def handle_identity_change(self, identity):
        node = self.model.handle_identity_change(identity)
        if node:
            self.view.update_connection(node)

    def handle_view_change(self, raw_data):
        """
        Handle view change
        :param dict raw_data:
        :return:
        """
        user_identity = raw_data.get("user_identity", None)
        currency = raw_data.get("currency", None)
        if user_identity != self.model.current_data("user_identity"):
            self.account_changed.emit(user_identity)
        if currency != self.model.current_data("currency"):
            self.currency_changed.emit(currency)
        self.model.set_current_data(raw_data)

    def add_connection(self, connection):
        raw_node = self.model.add_connection(connection)
        self.view.add_connection(raw_node)
        self.parse_node(raw_node)

    def tree_context_menu(self, point):
        mapped = self.view.splitter.mapFromParent(point)
        index = self.view.tree_view.indexAt(mapped)
        raw_data = self.view.tree_view.model().data(
            index, GenericTreeModel.ROLE_RAW_DATA
        )
        if raw_data:
            menu = QMenu(self.view)
            if raw_data["misc"]["connection"].uid:
                action_view_in_wot = QAction(
                    QCoreApplication.translate(
                        "NavigationController", "View in Web of Trust"
                    ),
                    menu,
                )
                menu.addAction(action_view_in_wot)
                action_view_in_wot.triggered.connect(
                    lambda c: self.model.view_in_wot(raw_data["misc"]["connection"])
                )

                action_gen_revocation = QAction(
                    QCoreApplication.translate(
                        "NavigationController", "Save revocation document"
                    ),
                    menu,
                )
                menu.addAction(action_gen_revocation)
                action_gen_revocation.triggered.connect(
                    lambda c: self.action_save_revocation(
                        raw_data["misc"]["connection"]
                    )
                )

                action_publish_uid = QAction(
                    QCoreApplication.translate("NavigationController", "Publish UID"),
                    menu,
                )
                menu.addAction(action_publish_uid)
                action_publish_uid.triggered.connect(
                    lambda c: self.publish_uid(raw_data["misc"]["connection"])
                )
                identity_published = self.model.identity_published(
                    raw_data["misc"]["connection"]
                )
                action_publish_uid.setEnabled(not identity_published)

                action_export_identity = QAction(
                    QCoreApplication.translate(
                        "NavigationController", "Export identity document"
                    ),
                    menu,
                )
                menu.addAction(action_export_identity)
                action_export_identity.triggered.connect(
                    lambda c: self.export_identity_document(
                        raw_data["misc"]["connection"]
                    )
                )

                action_leave = QAction(
                    QCoreApplication.translate(
                        "NavigationController", "Leave the currency"
                    ),
                    menu,
                )
                menu.addAction(action_leave)
                action_leave.triggered.connect(
                    lambda c: self.send_leave(raw_data["misc"]["connection"])
                )
                action_leave.setEnabled(
                    self.model.identity_is_member(raw_data["misc"]["connection"])
                )

            copy_pubkey = QAction(
                QCoreApplication.translate(
                    "NavigationController", "Copy pubkey to clipboard"
                ),
                menu.parent(),
            )
            copy_pubkey.triggered.connect(
                lambda checked, c=raw_data["misc"][
                    "connection"
                ]: NavigationModel.copy_pubkey_to_clipboard(c)
            )
            menu.addAction(copy_pubkey)

            copy_pubkey_crc = QAction(
                QCoreApplication.translate(
                    "NavigationController", "Copy pubkey to clipboard (with CRC)"
                ),
                menu.parent(),
            )
            copy_pubkey_crc.triggered.connect(
                lambda checked, c=raw_data["misc"][
                    "connection"
                ]: NavigationModel.copy_pubkey_to_clipboard_with_crc(c)
            )
            menu.addAction(copy_pubkey_crc)

            action_remove = QAction(
                QCoreApplication.translate(
                    "NavigationController", "Remove the Sakia account"
                ),
                menu,
            )
            menu.addAction(action_remove)
            action_remove.triggered.connect(
                lambda c: self.remove_connection(raw_data["misc"]["connection"])
            )
            # Show the context menu.

            menu.popup(QCursor.pos())

    @asyncify
    async def publish_uid(self, connection):
        identity = self.model.generate_identity(connection)
        identity_doc = identity.document()
        if not identity_doc.signatures:
            secret_key, password = await PasswordInputController.open_dialog(
                self, connection
            )
            if not password or not secret_key:
                return
            key = SigningKey.from_credentials(
                secret_key, password, connection.scrypt_params
            )
            identity_doc.sign([key])
            identity.signature = identity_doc.signatures[0]
            self.model.update_identity(identity)

        result = await self.model.send_identity(connection, identity_doc)
        if result[0]:
            if self.model.notifications():
                toast.display(
                    QCoreApplication.translate("NavigationController", "UID"),
                    QCoreApplication.translate(
                        "NavigationController", "Success publishing your UID"
                    ),
                )
            else:
                await QAsyncMessageBox.information(
                    self.view,
                    QCoreApplication.translate("NavigationController", "UID"),
                    QCoreApplication.translate(
                        "NavigationController", "Success publishing your UID"
                    ),
                )
        else:
            if not self.model.notifications():
                toast.display(
                    QCoreApplication.translate("NavigationController", "UID"), result[1]
                )
            else:
                await QAsyncMessageBox.critical(
                    self.view,
                    QCoreApplication.translate("NavigationController", "UID"),
                    result[1],
                )

    @asyncify
    async def send_leave(self):
        reply = await QAsyncMessageBox.warning(
            self,
            QCoreApplication.translate("NavigationController", "Warning"),
            QCoreApplication.translate(
                "NavigationController",
                """Are you sure?
Sending a leaving demand  cannot be canceled.
The process to join back the community later will have to be done again.""",
            ).format(self.account.pubkey),
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if reply == QMessageBox.Ok:
            connection = self.model.navigation_model.navigation.current_connection()
            secret_key, password = await PasswordInputController.open_dialog(
                self, connection
            )
            if not password or not secret_key:
                return
            result = await self.model.send_leave(connection, secret_key, password)
            if result[0]:
                if self.app.preferences["notifications"]:
                    toast.display(
                        QCoreApplication.translate("NavigationController", "Revoke"),
                        QCoreApplication.translate(
                            "NavigationController", "Success sending Revoke demand"
                        ),
                    )
                else:
                    await QAsyncMessageBox.information(
                        self,
                        QCoreApplication.translate("NavigationController", "Revoke"),
                        QCoreApplication.translate(
                            "NavigationController", "Success sending Revoke demand"
                        ),
                    )
            else:
                if self.app.preferences["notifications"]:
                    toast.display(
                        QCoreApplication.translate("NavigationController", "Revoke"),
                        result[1],
                    )
                else:
                    await QAsyncMessageBox.critical(
                        self,
                        QCoreApplication.translate("NavigationController", "Revoke"),
                        result[1],
                    )

    @asyncify
    async def remove_connection(self, connection):
        reply = await QAsyncMessageBox.question(
            self.view,
            QCoreApplication.translate(
                "NavigationController", "Removing the Sakia account"
            ),
            QCoreApplication.translate(
                "NavigationController",
                """Are you sure? This won't remove your money
 neither your identity from the network.""",
            ),
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if reply == QMessageBox.Ok:
            await self.model.remove_connection(connection)
            self.init_navigation()

    @asyncify
    async def action_save_revocation(self, connection):
        secret_key, password = await PasswordInputController.open_dialog(
            self, connection
        )
        if not password or not secret_key:
            return

        raw_document, _ = self.model.generate_revocation(
            connection, secret_key, password
        )
        # Testable way of using a QFileDialog
        selected_files = await QAsyncFileDialog.get_save_filename(
            self.view,
            QCoreApplication.translate(
                "NavigationController", "Save a revocation document"
            ),
            "revocation-{uid}-{pubkey}-{currency}.txt".format(
                uid=connection.uid,
                pubkey=connection.pubkey[:8],
                currency=connection.currency,
            ),
            QCoreApplication.translate(
                "NavigationController", "All text files (*.txt)"
            ),
        )
        if selected_files:
            path = selected_files[0]
            if not path.endswith(".txt"):
                path = "{0}.txt".format(path)
            with open(path, "w") as save_file:
                save_file.write(raw_document)

            dialog = QMessageBox(
                QMessageBox.Information,
                QCoreApplication.translate("NavigationController", "Revocation file"),
                QCoreApplication.translate(
                    "NavigationController",
                    """<div>Your revocation document has been saved.</div>
<div><b>Please keep it in a safe place.</b></div>
The publication of this document will revoke your identity on the network.</p>""",
                ),
                QMessageBox.Ok,
            )
            dialog.setTextFormat(Qt.RichText)
            await dialog_async_exec(dialog)

    @asyncify
    async def export_identity_document(self, connection):
        identity = self.model.generate_identity(connection)
        identity_doc = identity.document()
        if not identity_doc.signatures[0]:
            secret_key, password = await PasswordInputController.open_dialog(
                self, connection
            )
            if not password or not secret_key:
                return
            key = SigningKey.from_credentials(
                secret_key, password, connection.scrypt_params
            )
            identity_doc.sign([key])
            identity.signature = identity_doc.signatures[0]
            self.model.update_identity(identity)

        selected_files = await QAsyncFileDialog.get_save_filename(
            self.view,
            QCoreApplication.translate(
                "NavigationController", "Save an identity document"
            ),
            "identity-{uid}-{pubkey}-{currency}.txt".format(
                uid=connection.uid,
                pubkey=connection.pubkey[:8],
                currency=connection.currency,
            ),
            QCoreApplication.translate(
                "NavigationController", "All text files (*.txt)"
            ),
        )
        if selected_files:
            path = selected_files[0]
            if not path.endswith(".txt"):
                path = "{0}.txt".format(path)
            with open(path, "w") as save_file:
                save_file.write(identity_doc.signed_raw())

            dialog = QMessageBox(
                QMessageBox.Information,
                QCoreApplication.translate("NavigationController", "Identity file"),
                QCoreApplication.translate(
                    "NavigationController",
                    """<div>Your identity document has been saved.</div>
Share this document to your friends for them to certify you.</p>""",
                ),
                QMessageBox.Ok,
            )
            dialog.setTextFormat(Qt.RichText)
            await dialog_async_exec(dialog)
