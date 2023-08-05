from pathlib import Path
from typing import List

from .crypto import _salt, encrypt, decrypt
from .record import VaultRecord
from .exceptions import ItemExists, ItemNotFound
from .constants import APPDATA
from .data import SetupFacts


def build_salt(path: Path) -> bytes:
    salt: bytes = _salt()
    with path.joinpath("salt").open("wb") as binio:
        binio.write(salt)
    return salt


def build_vault(path: Path, salt: bytes, password: str):
    enc_data: bytes = encrypt(salt, password, dict())
    with path.joinpath("vault").open("wb") as binio:
        binio.write(enc_data)


def fetch_salt(path: Path) -> bytes:
    with path.joinpath("salt").open("rb") as binio:
        return binio.read()


def fetch_vault(path: Path) -> bytes:
    with path.joinpath("vault").open("rb") as binio:
        return binio.read()


def dump_vault(path: Path, vault: bytes):
    # TODO: Unit test me 🧪
    with path.joinpath("vault").open("wb") as binio:
        binio.write(vault)


def add_item(item: dict, data: dict, force: bool = False):
    item_name = _validate_item_name(item)
    if item_name in data.keys() and not force:
        raise ItemExists(item_name)
    data[item_name] = item


def _validate_item_name(item: dict) -> str:
    raw_name: str = item.pop("name")  # raises KeyError
    small_name: str = raw_name.lower()
    snake_name: str = small_name.replace(" ", "_")
    return snake_name


def remove_item(name: str, data: dict):
    if name in data.keys():
        data.pop(name)
    else:
        raise ItemNotFound(name)


def get_item(name: str, data: dict) -> VaultRecord:
    if name in data.keys():
        record: VaultRecord = VaultRecord(name, **data.get(name))
        return record
    raise ItemNotFound(name)


def list_items(data: dict) -> List:
    return list(data.keys())


def fetch_artifacts(password: str) -> SetupFacts:
    """Returns artifacts needed for vault interaction.

    Raises:
        shushi.IncorrectPassword
    """
    salt: bytes = fetch_salt(APPDATA)
    vault: bytes = fetch_vault(APPDATA)
    decrypted: dict = decrypt(salt, password, vault)
    return SetupFacts(salt, vault, decrypted)
