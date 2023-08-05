from PyQt5.QtCore import QLocale, QDateTime, QCoreApplication
from PyQt5.QtWidgets import QWidget
from .user_information_uic import Ui_UserInformationWidget
from sakia.gui.widgets.busy import Busy


class UserInformationView(QWidget, Ui_UserInformationWidget):
    """
    User information view
    """

    def __init__(self, parent):
        """
        Constructor
        """
        super().__init__(parent)
        self.setupUi(self)
        self.busy = Busy(self)
        self.busy.hide()

    def display_identity_timestamps(
        self, pubkey, publish_time, join_date, mstime_remaining, nb_certs
    ):
        """
        Display identity timestamps in localized format
        :param str pubkey:
        :param int publish_time:
        :param int join_date:
        :return:
        """
        if join_date:
            localized_join_date = QLocale.toString(
                QLocale(),
                QDateTime.fromTime_t(join_date),
                QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
            )
        else:
            localized_join_date = "###"

        if publish_time:
            localized_publish_date = QLocale.toString(
                QLocale(),
                QDateTime.fromTime_t(publish_time),
                QLocale.dateTimeFormat(QLocale(), QLocale.ShortFormat),
            )
        else:
            localized_publish_date = "###"

        if mstime_remaining:
            days, remainder = divmod(mstime_remaining, 3600 * 24)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                localized_mstime_remaining = "{days} days".format(days=days)
            else:
                localized_mstime_remaining = "{hours} hours and {min} min.".format(
                    hours=hours, min=minutes
                )
        else:
            localized_mstime_remaining = "###"

        text = QCoreApplication.translate(
            "UserInformationView",
            """
            <table cellpadding="5">
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:} BAT</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:} BAT</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            """,
        ).format(
            QCoreApplication.translate("UserInformationView", "Public key"),
            pubkey,
            QCoreApplication.translate("UserInformationView", "UID Published on"),
            localized_publish_date,
            QCoreApplication.translate("UserInformationView", "Join date"),
            localized_join_date,
            QCoreApplication.translate("UserInformationView", "Expires in"),
            localized_mstime_remaining,
            QCoreApplication.translate("UserInformationView", "Certs. received"),
            nb_certs,
        )

        # close html text
        text += "</table>"

        # set text in label
        self.label_properties.setText(text)

    def display_uid(self, uid, member):
        """
        Display the uid in the label
        :param str uid:
        """
        status_label = (
            QCoreApplication.translate("UserInformationView", "Member")
            if member
            else QCoreApplication.translate("UserInformationView", "Not a member")
        )
        status_color = (
            "#00AA00"
            if member
            else QCoreApplication.translate("UserInformationView", "#FF0000")
        )
        text = "<b>{uid}</b> <p style='color: {status_color};'>({status_label})</p>".format(
            uid=uid, status_color=status_color, status_label=status_label
        )
        self.label_uid.setText(text)

    def show_busy(self):
        self.busy.show()

    def hide_busy(self):
        self.busy.hide()

    def clear(self):
        self.label_properties.setText("")
        self.label_uid.setText("")

    def resizeEvent(self, event):
        self.busy.resize(event.size())
        super().resizeEvent(event)
