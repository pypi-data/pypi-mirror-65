from dataclasses import dataclass


@dataclass
class SetupFacts:
    salt: bytes
    vault: bytes
    decrypted: dict
