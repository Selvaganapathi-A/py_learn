from dataclasses import dataclass


class InvalidTransaction(Exception):
    pass


@dataclass(slots=True)
class BackAccount:
    balance: float

    def deposit(self, amount: float):
        if amount <= 0:
            raise InvalidTransaction(self.balance)
        self.balance += amount
        # #
        # message: str = "Cash Deposit"
        # amnt = locale.currency(amount,
        #                        symbol=True,
        #                        grouping=True,
        #                        international=True)
        # after_balance = locale.currency(self.balance,
        #                                 symbol=True,
        #                                 grouping=True,
        #                                 international=True)
        # print(f"{message:<30} : {amnt:>24} : {after_balance:>24}")

    def withdraw(self, amount: float):
        if self.balance < 0 or self.balance < amount:
            raise InvalidTransaction(self.balance, amount)
        else:
            self.balance = self.balance - amount
        # #
        # message: str = "Withdrawn"
        # amnt = locale.currency(amount,
        #                        symbol=True,
        #                        grouping=True,
        #                        international=True)
        # after_balance = locale.currency(self.balance,
        #                                 symbol=True,
        #                                 grouping=True,
        #                                 international=True)
        # print(f"{message:<30} : {amnt:>24} : {after_balance:>24}")
        return amount
