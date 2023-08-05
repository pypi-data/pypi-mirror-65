from PyQt5.QtWidgets import QWidget, QDialogButtonBox
from PyQt5.QtCore import QEvent, Qt, QCoreApplication
from .password_input_uic import Ui_PasswordInputWidget


class PasswordInputView(QWidget, Ui_PasswordInputWidget):
    """
    The model of Navigation component
    """

    def __init__(self, parent):
        # construct from qtDesigner
        super().__init__(parent)
        self.setupUi(self)
        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.layout().addWidget(self.button_box)
        self.button_box.hide()
        font = self.edit_secret_key.font()
        font.setBold(False)
        self.edit_secret_key.setFont(font)
        self.edit_password.setFont(font)

    def error(self, text):
        self.label_info.setText(text)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

    def clear(self):
        self.edit_password.clear()
        self.edit_secret_key.clear()

    def valid(self):
        self.label_info.setText(
            QCoreApplication.translate("PasswordInputView", "Password is valid")
        )
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

    def changeEvent(self, event):
        """
        Intercepte LanguageChange event to translate UI
        :param QEvent QEvent: Event
        :return:
        """
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        return super(PasswordInputView, self).changeEvent(event)
