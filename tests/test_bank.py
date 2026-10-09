import os
import unittest


# Use test database before importing the main program
os.environ["DB_NAME"] = "bank_system_test"


from src.backend.bank_account_system import BankAccountSystem, SavingsAccount
from src.backend.db.database import connection, cursor
from src.backend.models.current_account import CurrentAccount
from src.backend.auth.auth_service import AuthService


class TestBankAccountSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Security check:
        # Tests are allowed to run only on bank_system_test
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        if database_name != "bank_system_test":
            raise RuntimeError(
                "Tests must only run on bank_system_test!"
            )

    def setUp(self):
        # Clean database before every test
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM accounts")
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM users")

        connection.commit()

        self.bank = BankAccountSystem()

    def tearDown(self):
        # Clean database after every test
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM accounts")
        cursor.execute("DELETE FROM customers")
        cursor.execute("DELETE FROM users")

        connection.commit()

    def test_create_customer(self):
        self.bank.create_customer(
            1,
            "Test User",
            "Essen",
            "12345678",
            "test@test.de"
        )

        cursor.execute(
            """
            SELECT *
            FROM customers
            WHERE customer_id = %s
            """,
            (1,)
        )

        result = cursor.fetchone()

        self.assertIsNotNone(result)

    def test_create_account(self):
        self.bank.create_customer(
            1,
            "Test User",
            "Essen",
            "123456",
            "test@test.de"
        )

        self.bank.create_account(
            "TEST001",
            1000,
            1
        )

        balance = self.bank.get_balance("TEST001")

        self.assertEqual(balance, 1000)

    def test_deposit(self):
        self.bank.create_account(
            "TEST002",
            1000
        )

        self.bank.deposit(
            "TEST002",
            200
        )

        balance = self.bank.get_balance("TEST002")

        self.assertEqual(balance, 1200)

    def test_withdraw(self):
        self.bank.create_account(
            "TEST003",
            1000
        )

        self.bank.withdraw(
            "TEST003",
            300
        )

        balance = self.bank.get_balance("TEST003")

        self.assertEqual(balance, 700)

    def test_insufficient_funds(self):
        self.bank.create_account(
            "TEST004",
            100
        )

        self.bank.withdraw(
            "TEST004",
            500
        )

        balance = self.bank.get_balance("TEST004")

        self.assertEqual(balance, 100)

    def test_transfer(self):
        self.bank.create_account(
            "TEST005",
            1000
        )

        self.bank.create_account(
            "TEST006",
            500
        )

        self.bank.transfer(
            "TEST005",
            "TEST006",
            200
        )

        balance_1 = self.bank.get_balance("TEST005")
        balance_2 = self.bank.get_balance("TEST006")

        self.assertEqual(balance_1, 800)
        self.assertEqual(balance_2, 700)

    def test_delete_account(self):
        self.bank.create_account(
            "TEST007",
            500
        )

        self.bank.delete_account("TEST007")

        with self.assertRaises(ValueError):
            self.bank.get_balance("TEST007")

    def test_savings_account_limit(self):
        savings = SavingsAccount()

        savings.create_account(
            "TEST008",
            1000
        )

        savings.withdraw(
            "TEST008",
            600
        )

        balance = savings.get_balance("TEST008")

        self.assertEqual(balance, 1000)

    def test_negative_deposit(self):
        self.bank.create_account(
            "TEST009",
            1000
        )

        self.bank.deposit(
            "TEST009",
            -100
        )

        balance = self.bank.get_balance("TEST009")

        self.assertEqual(balance, 1000)

    def test_negative_withdraw(self):
        self.bank.create_account(
            "TEST010",
            1000
        )

        self.bank.withdraw(
            "TEST010",
            -100
        )

        balance = self.bank.get_balance("TEST010")

        self.assertEqual(balance, 1000)

    def test_transfer_to_same_account(self):
        self.bank.create_account(
            "TEST011",
            1000
        )

        self.bank.transfer(
            "TEST011",
            "TEST011",
            200
        )

        balance = self.bank.get_balance("TEST011")

        self.assertEqual(balance, 1000)

    def test_transaction_saved_after_deposit(self):
        self.bank.create_account(
            "TEST012",
            1000
        )

        self.bank.deposit(
            "TEST012",
            200
        )

        cursor.execute(
            """
            SELECT type, amount
            FROM transactions
            WHERE account_number = %s
            """,
            ("TEST012",)
        )

        transaction = cursor.fetchone()

        self.assertIsNotNone(transaction)
        self.assertEqual(transaction[0], "Deposit")
        self.assertEqual(float(transaction[1]), 200.0)

    def test_current_account_overdraft(self):
        current = CurrentAccount(overdraft_limit=500)

        current.create_account(
            "TEST013",
            100
        )

        current.withdraw(
            "TEST013",
            400
        )

        balance = current.get_balance("TEST013")

        self.assertEqual(balance, -300)

    def test_current_account_overdraft_limit(self):
        current = CurrentAccount(overdraft_limit=500)

        current.create_account(
            "TEST014",
            100
        )

        current.withdraw(
            "TEST014",
            700
        )

        balance = current.get_balance("TEST014")

        self.assertEqual(balance, 100)

    def test_create_user_password_is_hashed(self):
        auth = AuthService()

        auth.create_user(
            "marwan",
            "12345678"
        )

        cursor.execute(
            """
            SELECT password_hash
            FROM users
            WHERE username = %s
            """,
            ("marwan",)
        )

        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertNotEqual(result[0], "12345678")

    def test_login_success(self):
        auth = AuthService()

        auth.create_user(
            "marwan",
            "12345678"
        )

        result = auth.login(
            "marwan",
            "12345678"
        )

        self.assertTrue(result)

    def test_login_wrong_password(self):
        auth = AuthService()

        auth.create_user(
            "marwan",
            "12345678"
        )

        result = auth.login(
            "marwan",
            "wrongpassword"
        )

        self.assertFalse(result)

    def test_login_user_not_found(self):
        auth = AuthService()

        result = auth.login(
            "unknown_user",
            "12345678"
        )

        self.assertFalse(result)

    def test_duplicate_username(self):
        auth = AuthService()

        first = auth.create_user(
            "marwan",
            "12345678"
        )

        second = auth.create_user(
            "marwan",
            "abcdefgh"
        )

        self.assertTrue(first)
        self.assertFalse(second)

    def test_user_role_is_user_by_default(self):
        auth = AuthService()

        auth.create_user(
            "marwan",
            "12345678"
        )

        cursor.execute(
            """
            SELECT role
            FROM users
            WHERE username = %s
            """,
            ("marwan",)
        )

        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "USER")

    def test_short_password_is_rejected(self):
        auth = AuthService()

        result = auth.create_user(
            "marwan",
            "123456"
        )

        self.assertFalse(result)

    def test_short_username_is_rejected(self):
        auth = AuthService()

        result = auth.create_user(
            "ma",
            "12345678"
        )

        self.assertFalse(result)

    def test_empty_username_is_rejected(self):
        auth = AuthService()

        result = auth.create_user(
            "",
            "12345678"
        )

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()