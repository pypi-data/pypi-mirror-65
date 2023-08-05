import asyncio
import logging

from PyQt5.QtCore import QTime, pyqtSignal, QObject, QDateTime, QCoreApplication
from PyQt5.QtGui import QCursor

from sakia.decorators import asyncify
from sakia.gui.widgets import toast
from sakia.gui.widgets.context_menu import ContextMenu
from sakia.gui.sub.transfer.controller import TransferController
from .model import TxHistoryModel
from .view import TxHistoryView


class TxHistoryController(QObject):
    """
    Transfer history component controller
    """

    view_in_wot = pyqtSignal(object)

    def __init__(self, view, model, transfer):
        """

        :param TxHistoryView view:
        :param TxHistoryModel model:
        :param sakia.gui.sub.transfer.controller.TransferController transfer:
        """
        super().__init__()
        self.view = view
        self.model = model
        self.transfer = transfer
        self._logger = logging.getLogger("sakia")
        ts_from, ts_to = self.view.get_time_frame()
        model = self.model.init_history_table_model(ts_from, ts_to)
        self.view.set_table_history_model(model)

        self.view.date_from.dateChanged.connect(self.dates_changed)
        self.view.date_to.dateChanged.connect(self.dates_changed)
        self.view.table_history.customContextMenuRequested["QPoint"].connect(
            self.history_context_menu
        )
        self.view.button_refresh.clicked.connect(self.refresh_from_network)
        self.refresh()

    @classmethod
    def create(
        cls,
        parent,
        app,
        connection,
        identities_service,
        blockchain_service,
        transactions_service,
        sources_service,
    ):

        controller = TransferController.integrate_to_main_view(None, app, connection)
        view = TxHistoryView(parent.view, controller.view)
        model = TxHistoryModel(
            None,
            app,
            connection,
            blockchain_service,
            identities_service,
            transactions_service,
            sources_service,
        )
        txhistory = cls(view, model, controller)
        model.setParent(txhistory)
        app.referential_changed.connect(txhistory.refresh_balance)
        app.sources_refreshed.connect(txhistory.refresh_balance)
        txhistory.view_in_wot.connect(app.view_in_wot)
        txhistory.view.spin_page.valueChanged.connect(model.change_page)
        controller.accepted.connect(view.clear)
        controller.rejected.connect(view.clear)
        return txhistory

    def refresh_minimum_maximum(self):
        """
        Refresh minimum and maximum datetime
        """
        minimum, maximum = self.model.minimum_maximum_datetime()
        self.view.set_minimum_maximum_datetime(minimum, maximum)

    def refresh(self):
        self.refresh_minimum_maximum()
        self.refresh_balance()
        self.refresh_pages()

    @asyncify
    async def notification_reception(self, received_list):
        if len(received_list) > 0:
            localized_amount = await self.model.received_amount(received_list)
            text = QCoreApplication.translate(
                "TxHistoryController", "Received {amount} from {number} transfers"
            ).format(amount=localized_amount, number=len(received_list))
            if self.model.notifications():
                toast.display(
                    QCoreApplication.translate(
                        "TxHistoryController", "New transactions received"
                    ),
                    text,
                )

    def refresh_balance(self):
        localized_amount = self.model.localized_balance()
        self.view.set_balance(localized_amount)

    def refresh_pages(self):
        pages = self.model.max_pages()
        self.view.set_max_pages(pages)

    def history_context_menu(self, point):
        index = self.view.table_history.indexAt(point)
        valid, identities, transfer = self.model.table_data(index)
        if valid:
            menu = ContextMenu.from_data(
                self.view,
                self.model.app,
                self.model.connection,
                identities + [transfer],
            )
            menu.view_identity_in_wot.connect(self.view_in_wot)
            cursor = QCursor.pos()
            _x = cursor.x()
            _y = cursor.y()

            # Show the context menu.
            menu.qmenu.popup(cursor)

    def dates_changed(self):
        self._logger.debug("Changed dates")
        if self.view.table_history.model():
            # capture datetimes from calendar widget
            qdate_from = self.view.date_from.dateTime()  # type: QDateTime
            qdate_to = self.view.date_to.dateTime()  # type: QDateTime
            # time is midnight
            qdate_from.setTime(QTime(0, 0, 0))
            qdate_to.setTime(QTime(0, 0, 0))

            # calculate dates
            qdate_from_plus_one_year = qdate_from.addYears(1)
            qdate_to_minus_one_month = qdate_to.addMonths(-1)
            qone_month_ago = QDateTime.currentDateTime().addMonths(-1)
            qtomorrow = QDateTime.currentDateTime().addDays(1)
            qtomorrow.setTime(QTime(0, 0, 0))

            # if start later than one month ago...
            if qdate_from > qone_month_ago:
                # start = now - 1 month
                qdate_from = qone_month_ago

            # if start > end minus one month...
            if qdate_from > qdate_to_minus_one_month:
                # end = start + 1 month
                qdate_to = qdate_from.addMonths(1)

            # if period is more than one year long...
            if qdate_to > qdate_from_plus_one_year:
                # end = start + 1 year
                qdate_to.setDate(qdate_from_plus_one_year.date())

            # if end > tomorrow...
            if qdate_to > qtomorrow:
                # end = tomorrow
                qdate_to = qtomorrow

            # todo: update minimum and maximum of the calendar to forbid bad dates
            # update calendar
            self.view.date_from.setDateTime(qdate_from)
            self.view.date_to.setDateTime(qdate_to)

            # update model in table
            ts_from = qdate_from.toTime_t()
            ts_to = qdate_to.toTime_t()
            self.view.table_history.model().set_period(ts_from, ts_to)

            # refresh
            self.refresh_balance()
            self.refresh_pages()

    @asyncify
    async def refresh_from_network(self, _):
        """
        Update tx history from network for the selected date period
        :return:
        """
        self._logger.debug("Manually update tx history...")

        # disable update button
        self.view.button_refresh.setDisabled(True)

        pubkey = self.model.connection.pubkey
        try:
            (
                changed_tx,
                new_tx,
            ) = await self.model.transactions_service.update_transactions_history(
                pubkey,
                self.view.table_history.model().ts_from,
                self.view.table_history.model().ts_to,
            )
            for tx in changed_tx:
                self.model.app.transaction_state_changed.emit(tx)

            for tx in new_tx:
                self.model.app.new_transfer.emit(self.model.connection, tx)
        except Exception as e:
            self._logger.error(str(e))

        try:
            new_dividends = await self.model.transactions_service.update_dividends_history(
                pubkey,
                self.view.table_history.model().ts_from,
                self.view.table_history.model().ts_to,
                new_tx,
            )
            self._logger.debug("Found {} new dividends".format(len(new_dividends)))

            for ud in new_dividends:
                self.model.app.new_dividend.emit(self.model.connection, ud)
        except Exception as e:
            self._logger.error(str(e))

        # enable update button
        self.view.button_refresh.setDisabled(False)
        self._logger.debug("Manually update tx history finished")
