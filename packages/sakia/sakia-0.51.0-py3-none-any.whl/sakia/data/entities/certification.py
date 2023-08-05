import attr
from duniterpy.documents import block_uid, BlockUID


@attr.s(hash=True)
class Certification:
    currency = attr.ib(converter=str)
    certifier = attr.ib(converter=str)
    certified = attr.ib(converter=str)
    block = attr.ib(converter=int)
    timestamp = attr.ib(converter=int, cmp=False)
    signature = attr.ib(converter=str, cmp=False, hash=False)
    written_on = attr.ib(converter=int, default=-1, cmp=False, hash=False)
