from dataclasses import dataclass
from typing import List

from exercise2.transaction_registry import Transaction
from simple_cryptography import hash


@dataclass
class Block:
    """
    Blok powinien zawierać:
    - hash poprzedniego bloku,
    - moment w czasie, w którym został stworzony,
    - listę transakcji
    - nonce.
    """
    prev_block_hash: bytes
    timestamp: int
    nonce: int
    transactions: List[Transaction]

    @property
    def hash(self):
        hashed = b"\x00"
        for transaction in self.transactions:
            hashed = hash(transaction.tx_hash + hashed)
        return hash(
            self.prev_block_hash
            + self.timestamp.to_bytes(32, "big")
            + self.nonce.to_bytes(32, "big")
            + hashed
        )