from .constants import APPDATA
from .core import (add_item, build_salt, build_vault, dump_vault, encrypt,
                   fetch_artifacts, get_item, list_items, remove_item)
from .exceptions import VaultExists
from .record import VaultRecord


def make(password: str, force: bool = False):
    """
    Raises:
        shushi.exceptions.VaultExists
    """
    if not APPDATA.joinpath("vault").is_file() or force:
        salt: bytes = build_salt(APPDATA)
        build_vault(APPDATA, salt, password)
    else:
        raise VaultExists(APPDATA)


def add(item: dict, password: str, force: bool = False):
    """
    Raises:
        shushi.exceptions.IncorrectPassword
        shushi.exceptions.ItemExists
    """
    facts = fetch_artifacts(password)
    add_item(item, facts.decrypted, force)
    encrypted: bytes = encrypt(facts.salt, password, facts.decrypted)
    dump_vault(APPDATA, encrypted)


def get(name: str, password: str) -> VaultRecord:
    """
    Raises:
        shushi.exceptions.IncorrectPassword
        shushi.exceptions.ItemNotFound
    """
    facts = fetch_artifacts(password)
    return get_item(name, facts.decrypted)


def remove(name: str, password: str):
    """
    Rasies:
        shushi.exceptions.IncorrectPassword
        shushi.exceptions.ItemNotFound
    """
    facts = fetch_artifacts(password)
    remove_item(name, facts.decrypted)
    encrypted: bytes = encrypt(facts.salt, password, facts.decrypted)
    dump_vault(APPDATA, encrypted)


def list_names(password: str):
    """
    Raises:
        shushi.exceptions.IncorrectPassword
    """
    facts = fetch_artifacts(password)
    return list_items(facts.decrypted)
