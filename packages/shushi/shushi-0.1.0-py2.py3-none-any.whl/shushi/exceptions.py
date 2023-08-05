from click import ClickException


class ShushiException(ClickException):
    """Base exception."""
    def __init__(self, message=None, **kwargs):
        if not message:
            message = "Shushi encountered a problem."
        ClickException.__init__(self, message)


class IncorrectPassword(ShushiException):
    """Supplied password was incorrect."""


class ItemExists(ShushiException):
    """Supplied item already exists in the vault."""
    def __init__(self, item: str, *args, **kwargs):
        self.item = item
        message = f"An item named [{item}] already exists."
        ShushiException.__init__(self, message)


class ItemNotFound(ShushiException):
    """Supplied item could not be found."""
    def __init__(self, item: str, *args, **kwargs):
        self.item = item
        message = f"An item named [{item}] could not be found."
        ShushiException.__init__(self, message)


class VaultExists(ShushiException):
    """Vault already exists at this path."""
    def __init__(self, item: str, *args, **kwargs):
        self.item = item
        message = f"An vault already exists at [{item}]."
        ShushiException.__init__(self, message)
