from unittest import TestCase

from py_learn.unittest_example.bank import BackAccount, InvalidTransactionError


class TestBankAccount(TestCase):
    def setUp(self):
        # Initialize a bank account with a balance of 1000 for testing
        self.account = BackAccount(balance=1000)
        return super().__init__()

    def tearDown(self) -> None:
        del self.account
        return super().tearDown()

    def test__deposit(self):
        # Test depositing a valid amount
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)
        # Test depositing a negative amount
        with self.assertRaises(InvalidTransactionError):
            self.account.deposit(-100)

    def test__withdraw(self):
        # Test withdrawing a valid amount
        self.account.withdraw(300)
        self.assertEqual(self.account.balance, 700)
        # Test withdrawing more than the balance
        with self.assertRaises(InvalidTransactionError):
            self.account.withdraw(1000)
