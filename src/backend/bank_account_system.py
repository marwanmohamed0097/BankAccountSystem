from abc import ABC, abstractmethod

from mysql.connector import Error, IntegrityError

from .db.database import get_connection


class Account(ABC):

    @abstractmethod
    def withdraw(self, account_number, amount):
        pass


class BankAccountSystem(Account):

    def _customer_exists(
        self,
        cursor,
        customer_id
    ):
        sql = """
        SELECT customer_id
        FROM customers
        WHERE customer_id = %s
        """

        cursor.execute(
            sql,
            (customer_id,)
        )

        return cursor.fetchone() is not None

    def _get_balance(
        self,
        cursor,
        account_number,
        for_update=False
    ):
        sql = """
        SELECT balance
        FROM accounts
        WHERE account_number = %s
        """

        if for_update:
            sql += " FOR UPDATE"

        cursor.execute(
            sql,
            (account_number,)
        )

        result = cursor.fetchone()

        if result is None:
            raise ValueError(
                "Account does not exist."
            )

        return result[0]

    def _save_transaction(
        self,
        cursor,
        account_number,
        transaction_type,
        amount
    ):
        sql = """
        INSERT INTO transactions (
            account_id,
            transaction_type,
            amount
        )
        SELECT id, %s, %s
        FROM accounts
        WHERE account_number = %s
        """

        cursor.execute(
            sql,
            (
                transaction_type,
                amount,
                account_number
            )
        )

    def create_customer(
        self,
        customer_id,
        name,
        address,
        phone,
        email
    ):
        connection = None
        cursor = None

        sql = """
        INSERT INTO customers (
            customer_id,
            name,
            address,
            phone,
            email
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            customer_id,
            name,
            address,
            phone,
            email
        )

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                sql,
                values
            )

            connection.commit()

            print("Customer created successfully")
            return True

        except IntegrityError:
            if connection:
                connection.rollback()

            print("Customer already exists.")
            return False

        except Error as error:
            if connection:
                connection.rollback()

            print("Database error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()

    def customer_exists(
        self,
        customer_id
    ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            return self._customer_exists(
                cursor,
                customer_id
            )

        except Error as error:
            print("Database error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()

    def create_account(
        self,
        account_number,
        initial_balance=0,
        customer_id=None,
        user_id=None
    ):
        if initial_balance < 0:
            print(
                "Initial balance cannot be negative."
            )
            return False

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            if customer_id is not None:
                customer_found = (
                    self._customer_exists(
                        cursor,
                        customer_id
                    )
                )

                if not customer_found:
                    print(
                        "Customer does not exist."
                    )
                    return False

            sql = """
            INSERT INTO accounts (
                account_number,
                balance,
                customer_id,
                user_id
            )
            VALUES (%s, %s, %s, %s)
            """

            values = (
                account_number,
                initial_balance,
                customer_id,
                user_id
            )

            cursor.execute(
                sql,
                values
            )

            connection.commit()

            print(
                "Account created successfully"
            )
            return True

        except IntegrityError:
            if connection:
                connection.rollback()

            print("Account already exists.")
            return False

        except Error as error:
            if connection:
                connection.rollback()

            print("Database error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()

    def save_transaction(
        self,
        account_number,
        transaction_type,
        amount
    ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            self._save_transaction(
                cursor,
                account_number,
                transaction_type,
                amount
            )

            connection.commit()
            return True

        except Error as error:
            if connection:
                connection.rollback()

            print(
                "Transaction save failed:",
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

    def deposit(
        self,
        account_number,
        amount
    ):
        if amount <= 0:
            print(
                "Deposit amount must be positive."
            )
            return False

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql,
                (
                    amount,
                    account_number
                )
            )

            if cursor.rowcount == 0:
                connection.rollback()

                print(
                    "Account does not exist."
                )
                return False

            self._save_transaction(
                cursor,
                account_number,
                "Deposit",
                amount
            )

            connection.commit()

            print("Deposit successful")
            return True

        except Error as error:
            if connection:
                connection.rollback()

            print(
                "Deposit failed:",
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

    def get_balance(
        self,
        account_number
    ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            return self._get_balance(
                cursor,
                account_number
            )

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()

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

            if balance < amount:
                connection.rollback()

                print(
                    "Insufficient funds."
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

    def transfer(
        self,
        from_account,
        to_account,
        amount
    ):
        if from_account == to_account:
            print(
                "Cannot transfer to the same account."
            )
            return False

        if amount <= 0:
            print(
                "Transfer amount must be positive."
            )
            return False

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            accounts = sorted(
                [
                    from_account,
                    to_account
                ]
            )

            balances = {}

            for account_number in accounts:
                try:
                    balances[account_number] = (
                        self._get_balance(
                            cursor,
                            account_number,
                            for_update=True
                        )
                    )

                except ValueError:
                    connection.rollback()

                    print(
                        "One of the accounts "
                        "does not exist."
                    )
                    return False

            from_balance = balances[
                from_account
            ]

            if from_balance < amount:
                connection.rollback()

                print(
                    "Insufficient funds."
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
                    from_account
                )
            )

            sql = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql,
                (
                    amount,
                    to_account
                )
            )

            self._save_transaction(
                cursor,
                from_account,
                "Transfer Out",
                amount
            )

            self._save_transaction(
                cursor,
                to_account,
                "Transfer In",
                amount
            )

            connection.commit()

            print("Transfer successful")
            return True

        except Error as error:
            if connection:
                connection.rollback()

            print(
                "Transfer failed:",
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

    def delete_account(
        self,
        account_number
    ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
            DELETE FROM accounts
            WHERE account_number = %s
            """

            cursor.execute(
                sql,
                (account_number,)
            )

            if cursor.rowcount == 0:
                connection.rollback()

                print(
                    "Account does not exist."
                )
                return False

            connection.commit()

            print(
                "Account deleted successfully"
            )
            return True

        except Error as error:
            if connection:
                connection.rollback()

            print(
                "Delete failed:",
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

    def show_transactions(self):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
            SELECT *
            FROM transactions
            """

            cursor.execute(sql)

            results = cursor.fetchall()

            if not results:
                print(
                    "No transactions."
                )
                return

            for transaction in results:
                print(transaction)

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()

    def show_account_transactions(
        self,
        account_number
    ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
            SELECT transactions.*
            FROM transactions
            JOIN accounts
                ON transactions.account_id = accounts.id
            WHERE accounts.account_number = %s
            """

            cursor.execute(
                sql,
                (account_number,)
            )

            results = cursor.fetchall()

            if not results:
                print(
                    "No transactions."
                )
                return

            for transaction in results:
                print(transaction)

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()

    def show_customer_accounts(
        self,
        customer_id
    ):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
            SELECT account_number, balance
            FROM accounts
            WHERE customer_id = %s
            """

            cursor.execute(
                sql,
                (customer_id,)
            )

            results = cursor.fetchall()

            if not results:
                print(
                    "Customer has no accounts."
                )
                return

            for account in results:
                print(account)

        finally:
            if cursor:
                cursor.close()

            if (
                connection
                and connection.is_connected()
            ):
                connection.close()


class SavingsAccount(
    BankAccountSystem
):

    def withdraw(
        self,
        account_number,
        amount
    ):
        if amount > 500:
            print(
                "Maximum withdrawal is 500 Euro."
            )
            return False

        return super().withdraw(
            account_number,
            amount
        )


if __name__ == "__main__":
    bank = BankAccountSystem()