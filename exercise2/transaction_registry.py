from simple_cryptography import hash, PublicKey, verify_signature
from dataclasses import dataclass
from typing import Optional, List
import copy


@dataclass
class Transaction:
    """
    Transakcja zawiera:
    - odbiorcę transakcji (klucz publiczny)
    - hash poprzedniej transakcji
    """
    recipient: PublicKey
    previous_tx_hash: bytes

    @property
    def tx_hash(self):
        return hash(self.recipient.to_bytes() + self.previous_tx_hash)

    def __init__(self, recipient: PublicKey, previous_tx_hash: bytes):
        self.recipient = recipient
        self.previous_tx_hash = previous_tx_hash

    def __repr__(self):
        return f"Tx(recipient: {self.recipient.to_bytes()[-6:]}.., prev_hash: {self.previous_tx_hash[:6]}..)"


@dataclass
class SignedTransaction(Transaction):
    """
    Podpisana transakcja zawiera dodatkowo:
    - Podpis transakcji, utworzony przy pomocy klucza prywatnego poprzedniego właściciela transakcji.
    """
    signature: bytes

    def __init__(self, recipient: PublicKey, previous_tx_hash: bytes, signature: bytes):
        super().__init__(recipient, previous_tx_hash)
        self.signature = signature

    @staticmethod
    def from_transaction(transaction: Transaction, signature: bytes):
        return SignedTransaction(transaction.recipient, transaction.previous_tx_hash, signature)

    def __repr__(self):
        return f"SignedTx(recipient: {self.recipient.to_bytes()[-6:]}.., prev_hash: {self.previous_tx_hash[:6]}.., signature: {self.signature[:6]})"


class TransactionRegistry:
    """
    Klasa reprezentująca publiczny rejestr transakcji. Odpowiada za przyjmowanie nowych transakcji i ich
    przechowywanie.
    """
    transactions: List[Transaction]

    def __init__(self, initial_transactions: List[Transaction]):
        self.transactions = copy.copy(initial_transactions)

    def get_transaction(self, tx_hash: bytes) -> Optional[Transaction]:
        for transaction in self.transactions:
            if transaction.tx_hash == tx_hash:
                return transaction
        return None

    def is_transaction_spent(self, tx_hash: bytes) -> bool:
        for transaction in self.transactions:
            if transaction.previous_tx_hash == tx_hash:
                return True
        return False

    def verify_transaction_signature(self, transaction: SignedTransaction) -> bool:
        if self.get_transaction(transaction.previous_tx_hash) is None:
            return False
        return verify_signature(self.get_transaction(transaction.previous_tx_hash).recipient, transaction.signature,
                                transaction.tx_hash)

    def add_transaction(self, transaction: SignedTransaction) -> bool:
        if self.is_transaction_spent(transaction) or not self.verify_transaction_signature(transaction):
            return False
        else:
            self.transactions.append(transaction)
            return True
