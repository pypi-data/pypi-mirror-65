import attr


@attr.s()
class UserParameters:
    """
    The user parameters entity
    """

    profile_name = attr.ib(converter=str, default="Default Profile")
    lang = attr.ib(converter=str, default="en")
    referential = attr.ib(converter=int, default=0)
    expert_mode = attr.ib(converter=bool, default=False)
    digits_after_comma = attr.ib(converter=int, default=2)
    maximized = attr.ib(converter=bool, default=False)
    notifications = attr.ib(converter=bool, default=True)
    enable_proxy = attr.ib(converter=bool, default=False)
    proxy_type = attr.ib(converter=int, default=0)
    proxy_address = attr.ib(converter=str, default="")
    proxy_port = attr.ib(converter=int, default=8080)
    proxy_user = attr.ib(converter=str, default="")
    proxy_password = attr.ib(converter=str, default="")
    dark_theme = attr.ib(converter=bool, default=False)

    def proxy(self):
        if self.enable_proxy is True:
            if self.proxy_user and self.proxy_password:
                return "http://{:}:{:}@{:}:{:}".format(
                    self.proxy_user,
                    self.proxy_password,
                    self.proxy_address,
                    self.proxy_port,
                )
            else:
                return "http://{0}:{1}".format(self.proxy_address, self.proxy_port)
