from enum import Enum

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from sakia.decorators import asyncify
from sakia.gui.widgets.dialogs import QAsyncMessageBox
from .revocation_uic import Ui_RevocationDialog


class RevocationView(QDialog, Ui_RevocationDialog):
    """
    Home screen view
    """

    class PublicationMode(Enum):
        ADDRESS = 0
        COMMUNITY = 1

    def __init__(self, parent):
        """
        Constructor
        """
        super().__init__(parent)
        self.setupUi(self)

        self.button_next.setEnabled(False)

        self.radio_address.toggled.connect(
            lambda c: self.publication_mode_changed(
                RevocationView.PublicationMode.ADDRESS
            )
        )
        self.radio_currency.toggled.connect(
            lambda c: self.publication_mode_changed(
                RevocationView.PublicationMode.COMMUNITY
            )
        )

    def publication_mode_changed(self, radio):
        self.edit_address.setEnabled(radio == RevocationView.PublicationMode.ADDRESS)
        self.spinbox_port.setEnabled(radio == RevocationView.PublicationMode.ADDRESS)
        self.combo_currency.setEnabled(
            radio == RevocationView.PublicationMode.COMMUNITY
        )

    def refresh_target(self):
        if self.radio_currency.isChecked():
            target = QCoreApplication.translate(
                "RevocationView",
                "All nodes of currency {name}".format(
                    name=self.combo_currency.currentText()
                ),
            )
        elif self.radio_address.isChecked():
            target = QCoreApplication.translate(
                "RevocationView",
                "Address {address}:{port}".format(
                    address=self.edit_address.text(), port=self.spinbox_port.value()
                ),
            )
        else:
            target = ""
        self.label_target.setText(
            """
<h4>Publication address</h4>
<div>{target}</div>
""".format(
                target=target
            )
        )

    def refresh_revocation_label(self, revoked_identity):
        if revoked_identity:
            text = QCoreApplication.translate(
                "RevocationView",
                """
<div>Identity revoked: {uid} (public key: {pubkey}...)</div>
<div>Identity signed on block: {timestamp}</div>
    """.format(
                    uid=revoked_identity.uid,
                    pubkey=revoked_identity.pubkey[:12],
                    timestamp=revoked_identity.timestamp,
                ),
            )

            self.label_revocation_content.setText(text)

            if self.radio_currency.isChecked():
                target = QCoreApplication.translate(
                    "RevocationView",
                    "All nodes of currency {name}".format(
                        name=self.combo_currency.currentText()
                    ),
                )
            elif self.radio_address.isChecked():
                target = QCoreApplication.translate(
                    "RevocationView",
                    "Address {address}:{port}".format(
                        address=self.edit_address.text(), port=self.spinbox_port.value()
                    ),
                )
            else:
                target = ""
            self.label_revocation_info.setText(
                """
<h4>Revocation document</h4>
<div>{text}</div>
<h4>Publication address</h4>
<div>{target}</div>
""".format(
                    text=text, target=target
                )
            )
        else:
            self.label_revocation_content.setText("")

    def select_revocation_file(self):
        """
        Get a revocation file using a file dialog
        :rtype: str
        """
        selected_files = QFileDialog.getOpenFileName(
            self,
            QCoreApplication.translate("RevocationView", "Load a revocation file"),
            "",
            QCoreApplication.translate("RevocationView", "All text files (*.txt)"),
        )
        selected_file = selected_files[0]
        return selected_file

    def malformed_file_error(self):
        QMessageBox.critical(
            self,
            QCoreApplication.translate("RevocationView", "Error loading document"),
            QCoreApplication.translate(
                "RevocationView", "Loaded document is not a revocation document"
            ),
            buttons=QMessageBox.Ok,
        )

    async def revocation_broadcast_error(self, error):
        await QAsyncMessageBox.critical(
            self,
            QCoreApplication.translate("RevocationView", "Error broadcasting document"),
            error,
        )

    def show_revoked_selfcert(self, selfcert):
        text = QCoreApplication.translate(
            "RevocationView",
            """
        <div>Identity revoked: {uid} (public key: {pubkey}...)</div>
        <div>Identity signed on block: {timestamp}</div>
            """.format(
                uid=selfcert.uid,
                pubkey=selfcert.pubkey[:12],
                timestamp=selfcert.timestamp,
            ),
        )
        self.label_revocation_content.setText(text)

    def set_currencies_names(self, names):
        self.combo_currency.clear()
        for name in names:
            self.combo_currency.addItem(name)
        self.radio_currency.setChecked(True)

    def ask_for_confirmation(self):
        answer = QMessageBox.warning(
            self,
            QCoreApplication.translate("RevocationView", "Revocation"),
            QCoreApplication.translate(
                "RevocationView",
                """<h4>The publication of this document will revoke your identity on the network.</h4>
        <li>
            <li> <b>This identity won't be able to join the WoT anymore.</b> </li>
            <li> <b>This identity won't be able to generate Universal Dividends anymore.</b> </li>
            <li> <b>This identity won't be able to certify identities anymore.</b> </li>
        </li>
        Please think twice before publishing this document.
        """,
            ),
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        return answer == QMessageBox.Ok

    @asyncify
    async def accept(self):
        await QAsyncMessageBox.information(
            self,
            QCoreApplication.translate("RevocationView", "Revocation broadcast"),
            QCoreApplication.translate(
                "RevocationView", "The document was successfully broadcasted."
            ),
        )
        super().accept()
