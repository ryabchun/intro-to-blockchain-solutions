# Funkcje hashujące

from dataclasses import dataclass
from simple_cryptography import hash


@dataclass
class Transaction:
    id: int
    target_id: int
    metadata: str

    def hash(self) -> bytes:
        bytes_id = self.id.to_bytes(2, 'big')
        bytes_target_id = self.target_id.to_bytes(2, 'big')
        bytes_metadata = bytes(self.metadata, 'utf-8')
        bytes_str = bytes_id + bytes_target_id + bytes_metadata
        return hash(bytes_str)
        raise NotImplementedError()
