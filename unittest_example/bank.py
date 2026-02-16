from dataclasses import dataclass


class InvalidTransactionError(Exception): ...


@dataclass(slots=True)
class BackAccount:
    balance: float

    def deposit(self, amount: float):
        if amount <= 0:
            raise InvalidTransactionError(self.balance)
        self.balance += amount

    def withdraw(self, amount: float):
        if self.balance < 0 or self.balance < amount:
            raise InvalidTransactionError(self.balance, amount)
        self.balance -= amount
        return amount
