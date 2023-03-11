from time import time
from typing import Optional

from exercise2.transaction_registry import Transaction, SignedTransaction
from exercise3.block import Block
from exercise3.blockchain import Blockchain
from simple_cryptography import PublicKey, verify_signature, generate_key_pair

# Spróbuj zmodyfikować `DIFFICULTY` i zobacz, jak wpłynie to na czas wydobywania bloku!
DIFFICULTY = 18  # Oznacza ilość zerowych bitów na początku hasha
MAX_256_INT = 2**256


class Node:
    """
    Klasa reprezentująca węzeł sieci. Odpowiada za dodawanie transakcji i tworzenie bloków.
    Powinna zawierać:
    - blockchain,
    - klucz publiczny właściciela, wykorzystywany do przypisywania nowych coin'ów do konta.
    """
    blockchain: Blockchain
    owner: PublicKey

    def __init__(self, owner_public_key: PublicKey, initial_transaction: Transaction):
        block = Block(b"\x00", int(time()), 0, [initial_transaction])
        self. blockchain = Blockchain([block])
        self.owner = owner_public_key


    def add_transaction(self, transaction: SignedTransaction):
        if not self.validate_transaction(transaction):
            raise Exception("Verification failed")
        new_transaction = Transaction(self.owner, b"\x00")
        block = Block(prev_block_hash=self.blockchain.get_latest_block().hash, timestamp=int(time()), nonce=0,
                      transactions=[transaction, new_transaction])
        block = self.find_nonce(block)
        self.blockchain.blocks.append(block)


    def find_nonce(self, block: Block) -> Optional[Block]:
        while int.from_bytes(block.hash, "big") >= MAX_256_INT >> DIFFICULTY:
            block.nonce += 1

        return block

    def validate_transaction(self, transaction: SignedTransaction) -> bool:
        if transaction.signature is None:
            return False

        prev_transaction = self.blockchain.get_transaction_by(tx_hash=transaction.previous_tx_hash)
        if prev_transaction is None:
            return False
        if self.blockchain.get_transaction_by(previous_tx_hash=transaction.previous_tx_hash) is not None:
            return False
        return verify_signature(prev_transaction.recipient, transaction.signature, transaction.tx_hash)


    def get_state(self) -> Blockchain:
        """
        Zwróć blockchain.
        """
        return self.blockchain


def validate_chain(chain: Blockchain) -> bool:
    if len(chain.blocks[0].transactions) != 1:
        return False
    for index, block in enumerate(chain.blocks[1:]):

        if block.prev_block_hash != chain.blocks[index].hash:
            return False
        if int.from_bytes(block.hash, "big") > MAX_256_INT >> DIFFICULTY:
            return False
        if block.timestamp < chain.blocks[index].timestamp:
            return False

        node = Node(generate_key_pair()[0], chain.blocks[0].transactions[0])
        flag = False

        for transaction in block.transactions:
            if transaction.previous_tx_hash == b"\00":
                if flag:
                    return False
                flag = True
                continue

            if not node.validate_transaction(transaction):
                return False

        node.blockchain.blocks.append(block)
    return True
