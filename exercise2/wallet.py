from simple_cryptography import PrivateKey, PublicKey, sign, generate_key_pair
from exercise2.transaction_registry import TransactionRegistry, Transaction, SignedTransaction
from typing import Optional, Tuple, List

class Wallet:
    public_key: PublicKey

    def __init__(self, key_pair: Tuple[PublicKey, PrivateKey]):
        self.public_key = key_pair[0]

        # W produkcyjnych warunkach należy szczególnie zadbać o bezpieczeństwo klucza prywatnego.
        # W przypadku naszych warsztatów nie musimy się tym przejmować.
        self._private_key = key_pair[1]

    def get_unspent_transactions(self, registry: TransactionRegistry) -> List[Transaction]:
        unspent_transactions = []
        for transaction in registry.transactions:
            if transaction.recipient == self.public_key:
                if not registry.is_transaction_spent(transaction.tx_hash):
                    unspent_transactions.append(transaction)
        return unspent_transactions

    def get_balance(self, registry: TransactionRegistry) -> int:
        unspent_transactions = self.get_unspent_transactions(registry)
        return len(unspent_transactions)

    def sign_transaction(self, transaction: Transaction) -> SignedTransaction:
        sign_transaction = sign(self._private_key, transaction.tx_hash)
        return SignedTransaction.from_transaction(transaction, sign_transaction)

    def transfer(self, registry: TransactionRegistry, recipient: PublicKey) -> bool:
        unspent_transactions = self.get_unspent_transactions(registry)
        if not unspent_transactions:
            return False
        unspent_transaction = self.get_unspent_transactions(registry)[0]
        transfer_transaction = Transaction(recipient, unspent_transaction.tx_hash)
        transfer_transaction = self.sign_transaction(transfer_transaction)
        return registry.add_transaction(transfer_transaction)




