import attr
import re
from sakia.helpers import attrs_tuple_of_str


@attr.s(hash=True)
class Contact:
    """
    A contact in the network currency
    """

    re_displayed_text = re.compile("([\w\s\d]+) < ((?![OIl])[1-9A-Za-z]{42,45}) >")

    currency = attr.ib(converter=str)
    name = attr.ib(converter=str)
    pubkey = attr.ib(converter=str)
    fields = attr.ib(converter=attrs_tuple_of_str, default="")
    contact_id = attr.ib(converter=int, default=-1)

    def displayed_text(self):
        return self.name + " < " + self.pubkey + " > "
