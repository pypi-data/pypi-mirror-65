import attr
from duniterpy.documents import block_uid, BlockUID
from duniterpy.documents import Identity as IdentityDoc


@attr.s(hash=True)
class Identity:
    currency = attr.ib(converter=str)
    pubkey = attr.ib(converter=str)
    uid = attr.ib(converter=str, default="")
    blockstamp = attr.ib(converter=block_uid, default=BlockUID.empty())
    signature = attr.ib(converter=str, default="", cmp=False, hash=False)
    # Mediantime of the block referenced by blockstamp
    timestamp = attr.ib(converter=int, default=0, cmp=False, hash=False)
    written = attr.ib(converter=bool, default=False, cmp=False, hash=False)
    revoked_on = attr.ib(converter=int, default=0, cmp=False, hash=False)
    outdistanced = attr.ib(converter=bool, default=True, cmp=False, hash=False)
    member = attr.ib(
        validator=attr.validators.instance_of(bool),
        default=False,
        cmp=False,
        hash=False,
    )
    membership_buid = attr.ib(
        converter=block_uid, default=BlockUID.empty(), cmp=False, hash=False
    )
    membership_timestamp = attr.ib(converter=int, default=0, cmp=False, hash=False)
    membership_written_on = attr.ib(converter=int, default=0, cmp=False, hash=False)
    membership_type = attr.ib(
        converter=str,
        default="",
        validator=lambda s, a, t: t in ("", "IN", "OUT"),
        cmp=False,
        hash=False,
    )
    sentry = attr.ib(converter=bool, default=False, cmp=False, hash=False)

    def document(self):
        """
        Creates a self cert document for a given identity
        :param sakia.data.entities.Identity identity:
        :return: the document
        :rtype: duniterpy.documents.Identity
        """
        return IdentityDoc(
            10, self.currency, self.pubkey, self.uid, self.blockstamp, self.signature
        )

    def is_obsolete(self, sig_window, current_time):
        expired = self.timestamp + sig_window <= current_time
        return not self.written and expired
