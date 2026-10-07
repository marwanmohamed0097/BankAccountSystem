from src.backend.bank_account_system import BankAccountSystem
<<<<<<< HEAD


class CurrentAccount(BankAccountSystem):
=======
from src.backend.db.database import connection, cursor


class CurrentAccount(BankAccountSystem):

>>>>>>> 664fd94 (Add CurrentAccount with overdraft support)
    def __init__(self, overdraft_limit=500):
        self.overdraft_limit = overdraft_limit

    def withdraw(self, account_number, amount):
<<<<<<< HEAD
=======

        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

>>>>>>> 664fd94 (Add CurrentAccount with overdraft support)
        balance = self.get_balance(account_number)

        if balance + self.overdraft_limit < amount:
            print("Overdraft limit exceeded.")
            return

        sql = """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_number = %s
        """

<<<<<<< HEAD
        from src.backend.db.database import connection, cursor

        try:
            cursor.execute(sql, (amount, account_number))
=======
        try:
            cursor.execute(
                sql,
                (amount, account_number)
            )
>>>>>>> 664fd94 (Add CurrentAccount with overdraft support)

            self.save_transaction(
                account_number,
                "Withdraw",
                amount
            )

            connection.commit()
<<<<<<< HEAD
=======

>>>>>>> 664fd94 (Add CurrentAccount with overdraft support)
            print("Withdrawal successful")

        except Exception as error:
            connection.rollback()
            print("Withdrawal failed:", error)