import dataclasses
from typing import List, Optional

from exercise2.transaction_registry import Transaction
from exercise3.block import Block


@dataclasses.dataclass
class Blockchain:
    """
    Klasa reprezentująca łańcuch bloków.
    Powinna zawierać:
    - listę bloków.
    """
    blocks: List[Block]

    def get_latest_block(self) -> Block:
        return self.blocks[-1]

    def length(self) -> int:
        return len(self.blocks)

    def get_transaction_by(
            self,
            tx_hash: Optional[bytes] = None,
            previous_tx_hash: Optional[bytes] = None
    ) -> Optional[Transaction]:
        if tx_hash is None:
            for block in self.blocks:
                for transaction in block.transactions:
                    if transaction.previous_tx_hash == previous_tx_hash:
                        return transaction
        else:
            for block in self.blocks:
                for transaction in block.transactions:
                    if transaction.tx_hash == tx_hash:
                        return transaction
