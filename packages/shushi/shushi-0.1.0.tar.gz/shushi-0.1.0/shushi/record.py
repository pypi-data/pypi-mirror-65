class VaultRecord:
    """
    A class to represent a vault record.

    This classes constructor takes an number of key/value pairs as
    kwargs and assigns each key as an attribute with it's corresponding
    value as the attribute value.
    """
    def __init__(self, name: str, **kwargs):
        self.name: str = name
        for key, val in kwargs.items():
            self.__setattr__(key, val)
