import attr


@attr.s(hash=True)
class Source:

    TYPE_TRANSACTION = "T"
    TYPE_DIVIDEND = "D"

    currency = attr.ib(converter=str)
    pubkey = attr.ib(converter=str)
    identifier = attr.ib(converter=str)
    noffset = attr.ib(converter=int)
    type = attr.ib(converter=str, validator=lambda i, a, s: s == "T" or s == "D")
    amount = attr.ib(converter=int, hash=False)
    base = attr.ib(converter=int, hash=False)
    conditions = attr.ib(converter=str, hash=False)
    used_by = attr.ib(hash=False, default=None)
