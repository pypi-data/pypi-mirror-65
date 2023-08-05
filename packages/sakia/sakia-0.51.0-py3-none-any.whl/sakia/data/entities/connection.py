import attr
from duniterpy.documents import block_uid, BlockUID
from duniterpy.key.scrypt_params import ScryptParams, SCRYPT_PARAMS


@attr.s(hash=True)
class Connection:
    """
    A connection represents a connection to a currency's network
    It is defined by the currency name, and the key informations
    used to connect to it. If the user is using an identity, it is defined here too.
    """

    currency = attr.ib(converter=str)
    pubkey = attr.ib(converter=str)
    uid = attr.ib(converter=str, default="", cmp=False, hash=False)
    scrypt_N = attr.ib(converter=int, default=SCRYPT_PARAMS["N"], cmp=False, hash=False)
    scrypt_r = attr.ib(converter=int, default=SCRYPT_PARAMS["r"], cmp=False, hash=False)
    scrypt_p = attr.ib(converter=int, default=SCRYPT_PARAMS["p"], cmp=False, hash=False)
    blockstamp = attr.ib(
        converter=block_uid, default=BlockUID.empty(), cmp=False, hash=False
    )
    salt = attr.ib(converter=str, init=False, default="", cmp=False, hash=False)
    password = attr.ib(init=False, converter=str, default="", cmp=False, hash=False)

    def is_identity(self):
        return self.uid is not ""

    def is_wallet(self):
        return self.uid is ""

    def title(self):
        return "@".join([self.uid, self.pubkey[:11]])

    @property
    def scrypt_params(self):
        return ScryptParams(self.scrypt_N, self.scrypt_r, self.scrypt_p)
