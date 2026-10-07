from src.backend.bank_account_system import BankAccountSystem
from src.backend.db.database import connection, cursor


class CurrentAccount(BankAccountSystem):

    def __init__(self, overdraft_limit=500):
        self.overdraft_limit = overdraft_limit

    def withdraw(self, account_number, amount):

        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

        balance = self.get_balance(account_number)

        if balance + self.overdraft_limit < amount:
            print("Overdraft limit exceeded.")
            return

        sql = """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_number = %s
        """

        try:
            cursor.execute(
                sql,
                (amount, account_number)
            )

            self.save_transaction(
                account_number,
                "Withdraw",
                amount
            )

            connection.commit()
            print("Withdrawal successful")

        except Exception as error:
            connection.rollback()
            print("Withdrawal failed:", error)
