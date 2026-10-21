from mysql.connector import Error

from src.backend.bank_account_system import (
    BankAccountSystem
)
from src.backend.db.database import get_connection


class CurrentAccount(BankAccountSystem):

    def __init__(
        self,
        overdraft_limit=500
    ):
        self.overdraft_limit = (
            overdraft_limit
        )

    def withdraw(
        self,
        account_number,
        amount
    ):
        if amount <= 0:
            print(
                "Withdrawal amount must be positive."
            )
            return False

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            try:
                balance = self._get_balance(
                    cursor,
                    account_number,
                    for_update=True
                )

            except ValueError:
                connection.rollback()

                print(
                    "Account does not exist."
                )
                return False

            if (
                balance
                + self.overdraft_limit
                < amount
            ):
                connection.rollback()

                print(
                    "Overdraft limit exceeded."
                )
                return False

            sql = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql,
                (
                    amount,
                    account_number
                )
            )

            self._save_transaction(
                cursor,
                account_number,
                "Withdraw",
                amount
            )

            connection.commit()

            print(
                "Withdrawal successful"
            )
            return True

        except Error as error:
            if connection:
                connection.rollback()

            print(
                "Withdrawal failed:",
                error
            )
            return False

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()