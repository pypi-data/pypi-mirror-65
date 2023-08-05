from PyQt5.QtWidgets import (
    QFrame,
    QAction,
    QMenu,
    QSizePolicy,
    QInputDialog,
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QLabel,
)
from sakia.gui.widgets.dialogs import dialog_async_exec
from PyQt5.QtCore import QObject, QT_TRANSLATE_NOOP, Qt, QLocale, QCoreApplication
from .toolbar_uic import Ui_SakiaToolbar
from .about_uic import Ui_AboutPopup
from .about_money_uic import Ui_AboutMoney
from .about_wot_uic import Ui_AboutWot
from sakia.helpers import timestamp_to_dhms, dpi_ratio


class ToolbarView(QFrame, Ui_SakiaToolbar):
    """
    The model of Navigation component
    """

    _action_revoke_uid_text = QT_TRANSLATE_NOOP(
        "ToolbarView", "Publish a revocation document"
    )

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        tool_menu = QMenu(
            QCoreApplication.translate("ToolbarView", "Tools"), self.toolbutton_menu
        )
        self.toolbutton_menu.setMenu(tool_menu)

        self.action_add_connection = QAction(
            QCoreApplication.translate("ToolbarView", "Add an Sakia account"), tool_menu
        )
        tool_menu.addAction(self.action_add_connection)

        self.action_revoke_uid = QAction(
            QCoreApplication.translate(
                "ToolbarView", ToolbarView._action_revoke_uid_text
            ),
            self,
        )
        tool_menu.addAction(self.action_revoke_uid)

        self.action_parameters = QAction(
            QCoreApplication.translate("ToolbarView", "Settings"), tool_menu
        )
        tool_menu.addAction(self.action_parameters)

        self.action_plugins = QAction(
            QCoreApplication.translate("ToolbarView", "Plugins manager"), tool_menu
        )
        tool_menu.addAction(self.action_plugins)

        tool_menu.addSeparator()

        about_menu = QMenu(
            QCoreApplication.translate("ToolbarView", "About"), tool_menu
        )
        tool_menu.addMenu(about_menu)

        self.action_about_money = QAction(
            QCoreApplication.translate("ToolbarView", "About Money"), about_menu
        )
        about_menu.addAction(self.action_about_money)

        self.action_about_referentials = QAction(
            QCoreApplication.translate("ToolbarView", "About Referentials"), about_menu
        )
        about_menu.addAction(self.action_about_referentials)

        self.action_about_wot = QAction(
            QCoreApplication.translate("ToolbarView", "About Web of Trust"), about_menu
        )
        about_menu.addAction(self.action_about_wot)

        self.action_about = QAction(
            QCoreApplication.translate("ToolbarView", "About Sakia"), about_menu
        )
        about_menu.addAction(self.action_about)

        self.action_exit = QAction(
            QCoreApplication.translate("ToolbarView", "Quit"), tool_menu
        )
        tool_menu.addAction(self.action_exit)

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setMaximumHeight(60)
        self.button_network.setIconSize(self.button_network.iconSize() * dpi_ratio())
        self.button_contacts.setIconSize(self.button_contacts.iconSize() * dpi_ratio())
        self.button_identity.setIconSize(self.button_identity.iconSize() * dpi_ratio())
        self.button_explore.setIconSize(self.button_explore.iconSize() * dpi_ratio())
        self.toolbutton_menu.setIconSize(self.toolbutton_menu.iconSize() * dpi_ratio())
        self.button_network.setFixedHeight(
            self.button_network.height() * dpi_ratio() + 5 * dpi_ratio()
        )
        self.button_contacts.setFixedHeight(
            self.button_contacts.height() * dpi_ratio() + 5 * dpi_ratio()
        )
        self.button_identity.setFixedHeight(
            self.button_identity.height() * dpi_ratio() + 5 * dpi_ratio()
        )
        self.button_explore.setFixedHeight(
            self.button_explore.height() * dpi_ratio() + 5 * dpi_ratio()
        )
        self.toolbutton_menu.setFixedHeight(
            self.toolbutton_menu.height() * dpi_ratio() + 5 * dpi_ratio()
        )

    async def ask_for_connection(self, connections):
        connections_titles = [c.title() for c in connections]
        input_dialog = QInputDialog()
        input_dialog.setComboBoxItems(connections_titles)
        input_dialog.setWindowTitle(
            QCoreApplication.translate("ToolbarView", "Membership")
        )
        input_dialog.setLabelText(
            QCoreApplication.translate("ToolbarView", "Select an account")
        )
        await dialog_async_exec(input_dialog)
        result = input_dialog.textValue()

        if input_dialog.result() == QDialog.Accepted:
            for c in connections:
                if c.title() == result:
                    return c

    def show_about_wot(self, params):
        """
        Set wot text from currency parameters
        :param sakia.data.entities.BlockchainParameters params: Parameters of the currency
        :return:
        """
        dialog = QDialog(self)
        about_dialog = Ui_AboutWot()
        about_dialog.setupUi(dialog)

        # set infos in label
        about_dialog.label_wot.setText(
            QCoreApplication.translate(
                "ToolbarView",
                """
            <table cellpadding="5">
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}%</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
<tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
</table>
""",
            ).format(
                QLocale().toString(params.sig_period / 86400, "f", 2),
                QCoreApplication.translate(
                    "ToolbarView", "Minimum delay between 2 certifications (days)"
                ),
                QLocale().toString(params.sig_validity / 86400, "f", 2),
                QCoreApplication.translate(
                    "ToolbarView", "Maximum validity time of a certification (days)"
                ),
                params.sig_qty,
                QCoreApplication.translate(
                    "ToolbarView",
                    "Minimum quantity of certifications to be part of the WoT",
                ),
                params.sig_stock,
                QCoreApplication.translate(
                    "ToolbarView",
                    "Maximum quantity of active certifications per member",
                ),
                QLocale().toString(params.sig_window / 86400, "f", 2),
                QCoreApplication.translate(
                    "ToolbarView",
                    "Maximum time a certification can wait before being in blockchain (days)",
                ),
                params.xpercent * 100,
                QCoreApplication.translate(
                    "ToolbarView",
                    "Minimum percent of sentries to reach to match the distance rule",
                ),
                params.ms_validity / 86400,
                QCoreApplication.translate(
                    "ToolbarView", "Maximum validity time of a membership (days)"
                ),
                params.step_max,
                QCoreApplication.translate(
                    "ToolbarView",
                    "Maximum distance between each WoT member and a newcomer",
                ),
            )
        )
        dialog.setWindowTitle(
            QCoreApplication.translate("ToolbarView", "Web of Trust rules")
        )
        dialog.exec()

    def show_about_money(self, params, currency, localized_data):
        dialog = QDialog(self)
        about_dialog = Ui_AboutMoney()
        about_dialog.setupUi(dialog)
        about_dialog.label_general.setText(self.general_text(localized_data))
        about_dialog.label_rules.setText(self.rules_text(localized_data))
        about_dialog.label_money.setText(self.money_text(params, currency))
        dialog.setWindowTitle(QCoreApplication.translate("ToolbarView", "Money rules"))
        dialog.exec()

    def show_about_referentials(self, referentials):
        dialog = QDialog(self)
        layout = QVBoxLayout(dialog)
        tabwidget = QTabWidget(dialog)
        layout.addWidget(tabwidget)
        for ref in referentials:
            widget = QWidget()
            layout = QVBoxLayout(widget)
            label = QLabel()
            label.setText(self.text_referential(ref))
            layout.addWidget(label)
            tabwidget.addTab(widget, ref.translated_name())
        dialog.setWindowTitle(QCoreApplication.translate("ToolbarView", "Referentials"))
        dialog.exec()

    def general_text(self, localized_data):
        """
        Fill the general text with given informations
        :return:
        """
        # set infos in label
        return QCoreApplication.translate(
            "ToolbarView",
            """
            <table cellpadding="5">
            <tr><td align="right"><b>{:}</b></div></td><td>{:} {:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:} {:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:} {:}</td></tr>
            <tr><td align="right"><b>{:2.2%} / {:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            </table>
            """,
        ).format(
            localized_data.get("ud", "####"),
            QCoreApplication.translate("ToolbarView", "Universal Dividend UD(t) in"),
            localized_data["diff_units"],
            localized_data.get("mass", "###"),
            QCoreApplication.translate("ToolbarView", "Monetary Mass M(t) in"),
            localized_data["units"],
            localized_data.get("members_count", "####"),
            QCoreApplication.translate("ToolbarView", "Members N(t)"),
            localized_data.get("mass_per_member", "####"),
            QCoreApplication.translate(
                "ToolbarView", "Monetary Mass per member M(t)/N(t) in"
            ),
            localized_data["diff_units"],
            localized_data.get("actual_growth", 0),
            QCoreApplication.translate("ToolbarView", "day"),
            QCoreApplication.translate(
                "ToolbarView", "Actual growth c = UD(t)/[M(t)/N(t)]"
            ),
            # todo: wait for accurate datetime of reevaluation
            # localized_data.get("ud_median_time_minus_1", "####"),
            # QCoreApplication.translate("ToolbarView", "Penultimate UD date and time (t-1)"),
            localized_data.get("ud_median_time", "####") + " BAT",
            QCoreApplication.translate("ToolbarView", "Last UD date and time (t)"),
            localized_data.get("next_ud_median_time", "####") + " BAT",
            QCoreApplication.translate("ToolbarView", "Next UD date and time (t+1)"),
            localized_data.get("next_ud_reeval", "####") + " BAT",
            QCoreApplication.translate("ToolbarView", "Next UD reevaluation (t+1)"),
        )

    def rules_text(self, localized_data):
        """
        Set text in rules
        :param dict localized_data:
        :return:
        """
        # set infos in label
        return QCoreApplication.translate(
            "ToolbarView",
            """
            <table cellpadding="5">
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            </table>
            """,
        ).format(
            QCoreApplication.translate("ToolbarView", "{:2.2%} / {:} days").format(
                localized_data["growth"], localized_data["dt_reeval_in_days"]
            ),
            QCoreApplication.translate(
                "ToolbarView",
                "Fundamental growth (c) / Reevaluation delta time (dt_reeval)",
            ),
            QCoreApplication.translate(
                "ToolbarView", "UDĞ(t) = UDĞ(t-1) + c²*M(t-1)/N(t)"
            ),
            QCoreApplication.translate("ToolbarView", "Universal Dividend (formula)"),
            # fixme: re-display when the computed dividend will be accurate (need accurate previous monetary mass,
            #  last mass just before reevaluation)
            # QCoreApplication.translate("ToolbarView", "{:} = {:} + {:}² * {:} / {:}").format(
            #     localized_data.get("ud_plus_1", "####"),
            #     localized_data.get("ud", "####"),
            #     localized_data.get("growth_per_dt", "##########"),
            #     localized_data.get("mass", "####"),
            #     localized_data.get("members_count", "####"),
            # ),
            # QCoreApplication.translate("ToolbarView", "Universal Dividend (computed)"),
        )

    def text_referential(self, ref):
        """
        Set text from referentials
        """
        # set infos in label
        ref_template = """
                <table cellpadding="5">
                <tr><th>{:}</th><td>{:}</td></tr>
                <tr><th>{:}</th><td>{:}</td></tr>
                <tr><th>{:}</th><td>{:}</td></tr>
                <tr><th>{:}</th><td>{:}</td></tr>
                </table>
                """
        return ref_template.format(
            QCoreApplication.translate("ToolbarView", "Name"),
            ref.translated_name(),
            QCoreApplication.translate("ToolbarView", "Units"),
            ref.units,
            QCoreApplication.translate("ToolbarView", "Formula"),
            ref.formula,
            QCoreApplication.translate("ToolbarView", "Description"),
            ref.description,
        )

    def money_text(self, params, currency):
        """
        Set text from money parameters
        :param sakia.data.entities.BlockchainParameters params: Parameters of the currency
        :param str currency: The currency
        """

        dt_dhms = timestamp_to_dhms(params.dt)
        if dt_dhms[0] > 0:
            dt_as_str = QCoreApplication.translate(
                "ToolbarView", "{:} day(s) {:} hour(s)"
            ).format(*dt_dhms)
        else:
            dt_as_str = QCoreApplication.translate("ToolbarView", "{:} hour(s)").format(
                dt_dhms[1]
            )
        if dt_dhms[2] > 0 or dt_dhms[3] > 0:
            dt_dhms += ", {:} minute(s) and {:} second(s)".format(*dt_dhms[1:])
        dt_reeval_dhms = timestamp_to_dhms(params.dt_reeval)
        dt_reeval_as_str = QCoreApplication.translate(
            "ToolbarView", "{:} day(s) {:} hour(s)"
        ).format(*dt_reeval_dhms)

        # set infos in label
        return QCoreApplication.translate(
            "ToolbarView",
            """
            <table cellpadding="5">
            <tr><td align="right"><b>{:2.2%}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:} {:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:}</b></td><td>{:}</td></tr>
            <tr><td align="right"><b>{:2.0%}</b></td><td>{:}</td></tr>
            </table>
            """,
        ).format(
            params.c,
            QCoreApplication.translate("ToolbarView", "Fundamental growth (c)"),
            params.ud0,
            QCoreApplication.translate(
                "ToolbarView", "Initial Universal Dividend UD(0) in"
            ),
            currency,
            dt_as_str,
            QCoreApplication.translate("ToolbarView", "Time period between two UD"),
            dt_reeval_as_str,
            QCoreApplication.translate(
                "ToolbarView", "Time period between two UD reevaluation"
            ),
            params.median_time_blocks,
            QCoreApplication.translate(
                "ToolbarView", "Number of blocks used for calculating median time"
            ),
            params.avg_gen_time,
            QCoreApplication.translate(
                "ToolbarView",
                "The average time in seconds for writing 1 block (wished time)",
            ),
            params.dt_diff_eval,
            QCoreApplication.translate(
                "ToolbarView",
                "The number of blocks required to evaluate again PoWMin value",
            ),
            params.percent_rot,
            QCoreApplication.translate(
                "ToolbarView",
                "The percent of previous issuers to reach for personalized difficulty",
            ),
        )

    def show_about(self, text):
        dialog = QDialog(self)
        about_dialog = Ui_AboutPopup()
        about_dialog.setupUi(dialog)
        about_dialog.label.setText(text)
        dialog.exec()
