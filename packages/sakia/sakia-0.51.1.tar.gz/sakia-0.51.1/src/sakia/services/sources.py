from PyQt5.QtCore import QObject, QT_TRANSLATE_NOOP
from duniterpy.api import bma, errors
from duniterpy.documents import Transaction as TransactionDoc
from duniterpy.grammars.output import Condition, SIG, CSV, CLTV, XHX
from duniterpy.documents import BlockUID
import logging
import pypeg2
from sakia.data.entities import Source, Transaction
import hashlib

EVALUATE_CONDITION_ERROR_SIG = QT_TRANSLATE_NOOP(
    "SourcesServices", "missing secret key for public key"
)
EVALUATE_CONDITION_ERROR_XHX = QT_TRANSLATE_NOOP(
    "SourcesServices", "missing password for hash"
)
EVALUATE_CONDITION_ERROR_CSV = QT_TRANSLATE_NOOP(
    "SourcesServices", "locked by a delay until"
)
EVALUATE_CONDITION_ERROR_CLTV = QT_TRANSLATE_NOOP("SourcesServices", "locked until")


class SourcesServices(QObject):
    """
    Source service is managing sources received
    to update data locally
    """

    def __init__(
        self,
        currency,
        sources_processor,
        connections_processor,
        transactions_processor,
        blockchain_processor,
        bma_connector,
    ):
        """
        Constructor the identities service

        :param str currency: The currency name of the community
        :param sakia.data.processors.SourcesProcessor sources_processor: the sources processor for given currency
        :param sakia.data.processors.ConnectionsProcessor connections_processor: the connections processor
        :param sakia.data.processors.TransactionsProcessor transactions_processor: the transactions processor
        :param sakia.data.processors.BlockchainProcessor blockchain_processor: the blockchain processor
        :param sakia.data.connectors.BmaConnector bma_connector: The connector to BMA API
        """
        super().__init__()
        self._sources_processor = sources_processor
        self._connections_processor = connections_processor
        self._transactions_processor = transactions_processor
        self._blockchain_processor = blockchain_processor
        self._bma_connector = bma_connector
        self.currency = currency
        self._logger = logging.getLogger("sakia")

    def get_one(self, **search):
        return self._sources_processor.get_one(**search)

    def amount(self, pubkey):
        return self._sources_processor.amount(self.currency, pubkey)

    def parse_transaction_outputs(self, pubkey, transaction):
        """
        Parse a transaction to extract sources

        :param str pubkey: Receiver pubkey
        :param sakia.data.entities.Transaction transaction:
        """
        txdoc = TransactionDoc.from_signed_raw(transaction.raw)
        for offset, output in enumerate(txdoc.outputs):
            if self.find_signature_in_condition(output.condition, pubkey):
                source = Source(
                    currency=self.currency,
                    pubkey=pubkey,
                    identifier=txdoc.sha_hash,
                    type=Source.TYPE_TRANSACTION,
                    noffset=offset,
                    amount=output.amount,
                    base=output.base,
                    conditions=pypeg2.compose(output.condition, Condition),
                )
                self._sources_processor.insert(source)

    def consume_sources_from_transaction_inputs(self, pubkey, transaction):
        """
        Parse a transaction to drop sources used in inputs

        :param str pubkey: Receiver pubkey
        :param sakia.data.entities.Transaction transaction:
        """
        txdoc = TransactionDoc.from_signed_raw(transaction.raw)
        for index, input in enumerate(txdoc.inputs):
            source = Source(
                currency=self.currency,
                pubkey=txdoc.issuers[0],
                identifier=input.origin_id,
                type=input.source,
                noffset=input.index,
                amount=input.amount,
                base=input.base,
                conditions="",
                used_by=None,
            )
            if source.pubkey == pubkey:
                self._sources_processor.consume((source,), transaction.sha_hash)

    def _parse_ud(self, pubkey, dividend):
        """
        Add source in db from UD

        :param str pubkey: Pubkey of UD issuer
        :param sakia.data.entities.Dividend dividend: Dividend instance
        :return:
        """
        source = Source(
            currency=self.currency,
            pubkey=pubkey,
            identifier=pubkey,
            type=Source.TYPE_DIVIDEND,
            noffset=dividend.block_number,
            amount=dividend.amount,
            base=dividend.base,
            conditions=pypeg2.compose(Condition.token(SIG.token(pubkey)), Condition),
        )
        self._sources_processor.insert(source)

    async def initialize_sources(self, pubkey, log_stream, progress):
        sources_data = await self._bma_connector.get(
            self.currency, bma.tx.sources, req_args={"pubkey": pubkey}
        )
        nb_sources = len(sources_data["sources"])
        for index, source in enumerate(sources_data["sources"]):
            log_stream("Parsing source ud/tx {:}/{:}".format(index, nb_sources))
            progress(1 / nb_sources)
            self.add_source(pubkey, source)

    async def check_destruction(self, pubkey, block_number, unit_base):
        amount = self._sources_processor.amount(self.currency, pubkey)
        if amount < 100 * 10 ** unit_base:
            if self._sources_processor.available(self.currency, pubkey):
                self._sources_processor.drop_all_of(self.currency, pubkey)
                timestamp = await self._blockchain_processor.timestamp(
                    self.currency, block_number
                )
                next_txid = self._transactions_processor.next_txid(
                    self.currency, block_number
                )
                sha_identifier = (
                    hashlib.sha256(
                        "Destruction{0}{1}{2}".format(
                            block_number, pubkey, amount
                        ).encode("ascii")
                    )
                    .hexdigest()
                    .upper()
                )
                destruction = Transaction(
                    currency=self.currency,
                    pubkey=pubkey,
                    sha_hash=sha_identifier,
                    written_block=block_number,
                    blockstamp=BlockUID.empty(),
                    timestamp=timestamp,
                    signatures=[],
                    issuers=[pubkey],
                    receivers=[],
                    amount=amount,
                    amount_base=0,
                    comment="Too low balance",
                    txid=next_txid,
                    state=Transaction.VALIDATED,
                    local=True,
                    raw="",
                )
                self._transactions_processor.commit(destruction)
                return destruction

    async def refresh_sources_of_pubkey(self, pubkey):
        """
        Refresh the sources for a given pubkey
        :param str pubkey:
        :return: the destruction of sources
        """
        sources_data = await self._bma_connector.get(
            self.currency, bma.tx.sources, req_args={"pubkey": pubkey}
        )
        self._sources_processor.drop_all_of(self.currency, pubkey)
        for source in sources_data["sources"]:
            self.add_source(pubkey, source)

    async def refresh_sources(self, connections):
        """

        :param list[sakia.data.entities.Connection] connections:
        :param dict[sakia.data.entities.Transaction] transactions:
        :param dict[sakia.data.entities.Dividend] dividends:
        :return: the destruction of sources
        """
        for conn in connections:
            _, current_base = self._blockchain_processor.last_ud(self.currency)
            # there can be bugs if the current base switch during the parsing of blocks
            # but since it only happens every 23 years and that its only on accounts having less than 100
            # this is acceptable I guess

            await self.refresh_sources_of_pubkey(conn.pubkey)

    def restore_sources(self, pubkey, tx):
        """
        Restore consumed sources and drop created sources of a cancelled tx

        :param str pubkey: Pubkey
        :param Transaction tx: Instance of tx entity
        """
        txdoc = TransactionDoc.from_signed_raw(tx.raw)
        for offset, output in enumerate(txdoc.outputs):
            source = Source(
                currency=self.currency,
                pubkey=pubkey,
                identifier=txdoc.sha_hash,
                type=Source.TYPE_TRANSACTION,
                noffset=offset,
                amount=output.amount,
                base=output.base,
                conditions=pypeg2.compose(output.condition, Condition),
            )
            # drop sources created by the canceled tx
            self._sources_processor.drop(source)
        # restore consumed sources
        self._sources_processor.restore_all(tx.sha_hash)

    def find_signature_in_condition(self, _condition, pubkey, result=False):
        """
        Recursive function to find a SIG(pubkey) in a Condition object

        :param Condition _condition: Condition instance
        :param str pubkey: Pubkey to find
        :param bool result: True if found
        :return:
        """
        if isinstance(_condition.left, Condition):
            result |= self.find_signature_in_condition(_condition.left, pubkey, result)
        if isinstance(_condition.right, Condition):
            result |= self.find_signature_in_condition(_condition.right, pubkey, result)
        if (
            isinstance(_condition.left, SIG)
            and _condition.left.pubkey == pubkey
            or isinstance(_condition.right, SIG)
            and _condition.right.pubkey == pubkey
        ):
            result |= True
        return result

    def add_source(self, pubkey, source):
        """
        Add a new source for the pubkey

        :param str pubkey: Pubkey concerned
        :param dict source: Source dict from api
        :return:
        """
        try:
            entity = Source(
                currency=self.currency,
                pubkey=pubkey,
                identifier=source["identifier"],
                type=source["type"],
                noffset=source["noffset"],
                amount=source["amount"],
                base=source["base"],
                conditions=source["conditions"],
                used_by=None,
            )
            self._sources_processor.insert(entity)
        except AttributeError as e:
            self._logger.error(str(e))

    def evaluate_condition(
        self,
        currency: str,
        condition: Condition,
        pubkeys: list,
        passwords: list,
        identifier: str,
        result: bool = False,
        _errors: list = None,
    ) -> tuple:
        """
        Evaluate a source lock condition
        Support multiple signatures and passwords

        :param str currency: Name of currency
        :param Condition condition: Condition instance
        :param [str] pubkeys: Keys to unlock condition
        :param [str] passwords: List of passwords
        :param str identifier: Source transaction identifier
        :param bool result: Evaluation result accumulator
        :param [tuple] _errors: List of tuple with infos on condition returning false (condition: str, message: str,
         param: str|int)
        :return:
        """
        left = False
        right = False
        # if left param is a condition...
        if isinstance(condition.left, Condition):
            # evaluate condition
            left, _errors = self.evaluate_condition(
                currency,
                condition.left,
                pubkeys,
                passwords,
                identifier,
                result,
                _errors,
            )
        # if right param is a condition...
        if isinstance(condition.right, Condition):
            # evaluate condition
            right, _errors = self.evaluate_condition(
                currency,
                condition.right,
                pubkeys,
                passwords,
                identifier,
                result,
                _errors,
            )
        # if left param is a SIG...
        if isinstance(condition.left, SIG):
            if condition.left.pubkey in pubkeys:
                left = True
            else:
                if _errors is None:
                    _errors = []
                _errors.append(
                    (
                        pypeg2.compose(condition.left),
                        EVALUATE_CONDITION_ERROR_SIG,
                        condition.left.pubkey,
                    )
                )

        # if left param is a CSV value...
        if isinstance(condition.left, CSV):
            # capture transaction of the source
            tx = self._transactions_processor.find_one_by_hash(identifier)
            if tx:
                # capture current blockchain time
                median_time = self._blockchain_processor.time(currency)
                locked_until = tx.timestamp + int(condition.left.time)
                # param is true if tx time + CSV delay <= blockchain time
                left = locked_until <= median_time
                if left is False:
                    if _errors is None:
                        _errors = []
                    _errors.append(
                        (
                            pypeg2.compose(condition.left),
                            EVALUATE_CONDITION_ERROR_CSV,
                            locked_until,
                        )
                    )

        # if left param is a CLTV value...
        if isinstance(condition.left, CLTV):
            # capture current blockchain time
            median_time = self._blockchain_processor.time(currency)
            locked_until = int(condition.left.timestamp)
            # param is true if CL:TV value <= blockchain time
            left = locked_until <= median_time
            if left is False:
                if _errors is None:
                    _errors = []
                _errors.append(
                    (
                        pypeg2.compose(condition.left),
                        EVALUATE_CONDITION_ERROR_CLTV,
                        locked_until,
                    )
                )

        # if left param is a XHX value...
        if isinstance(condition.left, XHX):
            left = condition.left.sha_hash in [
                hashlib.sha256(password).hexdigest().upper() for password in passwords
            ]
            if left is False:
                if _errors is None:
                    _errors = []
                _errors.append(
                    (
                        pypeg2.compose(condition.left),
                        EVALUATE_CONDITION_ERROR_XHX,
                        condition.left.sha_hash,
                    )
                )

        # if no op then stop evaluation...
        if not condition.op:
            return left, _errors

        # if right param is a SIG...
        if isinstance(condition.right, SIG):
            if condition.right.pubkey in pubkeys:
                right = True
            else:
                if _errors is None:
                    _errors = []
                _errors.append(
                    (
                        pypeg2.compose(condition.right),
                        EVALUATE_CONDITION_ERROR_SIG,
                        condition.right.pubkey,
                    )
                )

        # if right param is a CSV value...
        if isinstance(condition.right, CSV):
            # capture transaction of the source
            tx = self._transactions_processor.find_one_by_hash(identifier)
            if tx:
                # capture current blockchain time
                median_time = self._blockchain_processor.time(currency)
                locked_until = tx.timestamp + int(condition.right.time)
                # param is true if tx time + CSV delay <= blockchain time
                right = locked_until <= median_time
                if right is False:
                    if _errors is None:
                        _errors = []
                    _errors.append(
                        (
                            pypeg2.compose(condition.right),
                            EVALUATE_CONDITION_ERROR_CSV,
                            locked_until,
                        )
                    )

        # if right param is a CLTV value...
        if isinstance(condition.right, CLTV):
            # capture current blockchain time
            median_time = self._blockchain_processor.time(currency)
            locked_until = int(condition.right.timestamp)
            # param is true if CL:TV value <= blockchain time
            right = locked_until <= median_time
            if right is False:
                if _errors is None:
                    _errors = []
                _errors.append(
                    (
                        pypeg2.compose(condition.right),
                        EVALUATE_CONDITION_ERROR_CLTV,
                        locked_until,
                    )
                )

        # if right param is a XHX value...
        if isinstance(condition.right, XHX):
            right = condition.right.sha_hash in [
                hashlib.sha256(password).hexdigest().upper() for password in passwords
            ]
            if right is False:
                if _errors is None:
                    _errors = []
                _errors.append(
                    (
                        pypeg2.compose(condition.right),
                        EVALUATE_CONDITION_ERROR_XHX,
                        condition.right.sha_hash,
                    )
                )

        # if operator AND...
        if condition.op == "&&":
            return left & right, _errors

        # operator OR
        return left | right, _errors
