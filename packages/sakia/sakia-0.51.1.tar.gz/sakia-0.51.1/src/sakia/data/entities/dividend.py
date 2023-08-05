import attr


@attr.s(hash=True)
class Dividend:
    currency = attr.ib(converter=str, cmp=True, hash=True)
    pubkey = attr.ib(converter=str, cmp=True, hash=True)
    block_number = attr.ib(converter=int, cmp=True, hash=True)
    timestamp = attr.ib(converter=int)
    amount = attr.ib(converter=int, cmp=False, hash=False)
    base = attr.ib(converter=int, cmp=False, hash=False)
