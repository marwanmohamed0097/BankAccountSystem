from abc import ABC, abstractmethod

from mysql.connector import Error, IntegrityError

from database import connection, cursor


class Customer:
    def __init__(self, customer_id, name, address, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email


class Account(ABC):
    @abstractmethod
    def withdraw(self, account_number, amount):
        pass


class BankAccountSystem(Account):

    def create_customer(self, customer_id, name, address, phone, email):
        sql = """
        INSERT INTO customers (customer_id, name, address, phone, email)
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
            cursor.execute(sql, values)
            connection.commit()
            print("Customer created successfully")

        except IntegrityError:
            connection.rollback()
            print("Customer already exists.")

        except Error as error:
            connection.rollback()
            print("Database error:", error)


    def customer_exists(self, customer_id):
        sql = """
        SELECT customer_id
        FROM customers
        WHERE customer_id = %s
        """

        cursor.execute(sql, (customer_id,))
        result = cursor.fetchone()

        return result is not None


    def create_account(
        self,
        account_number,
        initial_balance=0,
        customer_id=None
    ):
        if initial_balance < 0:
            print("Initial balance cannot be negative.")
            return

        if customer_id is not None:
            if not self.customer_exists(customer_id):
                print("Customer does not exist.")
                return

        sql = """
        INSERT INTO accounts (account_number, balance, customer_id)
        VALUES (%s, %s, %s)
        """

        values = (
            account_number,
            initial_balance,
            customer_id
        )

        try:
            cursor.execute(sql, values)
            connection.commit()
            print("Account created successfully")

        except IntegrityError:
            connection.rollback()
            print("Account already exists.")

        except Error as error:
            connection.rollback()
            print("Database error:", error)


    def save_transaction(
        self,
        account_number,
        transaction_type,
        amount
    ):
        sql = """
        INSERT INTO transactions (account_number, type, amount)
        VALUES (%s, %s, %s)
        """

        values = (
            account_number,
            transaction_type,
            amount
        )

        cursor.execute(sql, values)


    def deposit(self, account_number, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return

        sql = """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_number = %s
        """

        try:
            cursor.execute(sql, (amount, account_number))

            if cursor.rowcount == 0:
                print("Account does not exist.")
                return

            self.save_transaction(
                account_number,
                "Deposit",
                amount
            )

            connection.commit()
            print("Deposit successful")

        except Error as error:
            connection.rollback()
            print("Deposit failed:", error)


    def get_balance(self, account_number):
        sql = """
        SELECT balance
        FROM accounts
        WHERE account_number = %s
        """

        cursor.execute(sql, (account_number,))
        result = cursor.fetchone()

        if result is None:
            raise ValueError("Account does not exist.")

        return result[0]


    def withdraw(self, account_number, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

        try:
            balance = self.get_balance(account_number)

        except ValueError:
            print("Account does not exist.")
            return

        if balance < amount:
            print("Insufficient funds.")
            return

        sql = """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_number = %s
        """

        try:
            cursor.execute(sql, (amount, account_number))

            self.save_transaction(
                account_number,
                "Withdraw",
                amount
            )

            connection.commit()
            print("Withdrawal successful")

        except Error as error:
            connection.rollback()
            print("Withdrawal failed:", error)


    def transfer(self, from_account, to_account, amount):
        if from_account == to_account:
            print("Cannot transfer to the same account.")
            return

        if amount <= 0:
            print("Transfer amount must be positive.")
            return

        try:
            from_balance = self.get_balance(from_account)
            self.get_balance(to_account)

        except ValueError:
            print("One of the accounts does not exist.")
            return

        if from_balance < amount:
            print("Insufficient funds.")
            return

        try:
            sql = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql,
                (amount, from_account)
            )

            sql = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql,
                (amount, to_account)
            )

            self.save_transaction(
                from_account,
                "Transfer Out",
                amount
            )

            self.save_transaction(
                to_account,
                "Transfer In",
                amount
            )

            connection.commit()
            print("Transfer successful")

        except Error as error:
            connection.rollback()
            print("Transfer failed:", error)


    def delete_account(self, account_number):
        sql = """
        DELETE FROM accounts
        WHERE account_number = %s
        """

        try:
            cursor.execute(sql, (account_number,))

            if cursor.rowcount == 0:
                print("Account does not exist.")
                return

            connection.commit()
            print("Account deleted successfully")

        except Error as error:
            connection.rollback()
            print("Delete failed:", error)


    def show_transactions(self):
        sql = """
        SELECT *
        FROM transactions
        """

        cursor.execute(sql)
        results = cursor.fetchall()

        if not results:
            print("No transactions.")
            return

        for transaction in results:
            print(transaction)


    def show_account_transactions(self, account_number):
        sql = """
        SELECT *
        FROM transactions
        WHERE account_number = %s
        """

        cursor.execute(sql, (account_number,))
        results = cursor.fetchall()

        if not results:
            print("No transactions.")
            return

        for transaction in results:
            print(transaction)


    def show_customer_accounts(self, customer_id):
        sql = """
        SELECT account_number, balance
        FROM accounts
        WHERE customer_id = %s
        """

        cursor.execute(sql, (customer_id,))
        results = cursor.fetchall()

        if not results:
            print("Customer has no accounts.")
            return

        for account in results:
            print(account)


class SavingsAccount(BankAccountSystem):

    def withdraw(self, account_number, amount):
        if amount > 500:
            print("Maximum withdrawal is 500 Euro.")
            return

        super().withdraw(account_number, amount)


if __name__ == "__main__":
    bank = BankAccountSystem()

    # Examples:
    # bank.create_customer(1, "Marwan", "Essen", "0123456789", "mail@example.de")
    # bank.create_account("111111", 1000, 1)
    # bank.deposit("111111", 200)
    # bank.withdraw("111111", 100)
    # print(bank.get_balance("111111"))
    # bank.show_account_transactions("111111")

    cursor.close()
    connection.close()