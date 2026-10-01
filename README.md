# Bank Account System

A Python-based bank account management system connected to a MySQL database.

The project demonstrates object-oriented programming, database integration, transaction handling, automated testing, and basic error handling.

## Features

- Create customers
- Create bank accounts
- Connect accounts to customers
- Deposit money
- Withdraw money
- Transfer money between accounts
- Check account balance
- Delete accounts
- Store transactions in MySQL
- Show all transactions
- Show transactions for a specific account
- Show all accounts of a customer
- Savings account with withdrawal limit
- Database rollback if a transfer fails
- Automated tests using `unittest`

## Technologies

- Python 3
- MySQL
- mysql-connector-python
- python-dotenv
- unittest
- Git
- GitHub

## Object-Oriented Programming

The project uses several OOP concepts:

- Classes and Objects
- Inheritance
- Polymorphism
- Abstraction
- Methods

Example:

```python
class SavingsAccount(BankAccountSystem):

    def withdraw(self, account_number, amount):

        if amount > 500:
            print("Maximum withdrawal is 500 Euro.")
            return

        super().withdraw(account_number, amount)
```

## Project Structure

```text
Bank/
├── BankAccountSystem.PY
├── database.py
├── test_bank.py
├── README.md
├── .gitignore
└── .env
```

The `.env` file contains database credentials and is excluded from GitHub.

## Database

The project uses a MySQL database called:

```text
bank_system
```

A separate database is used for automated tests:

```text
bank_system_test
```

The main tables are:

### customers

Stores customer information.

- customer_id
- name
- address
- phone
- email

### accounts

Stores bank account information.

- id
- account_number
- balance
- customer_id

### transactions

Stores account transactions.

- id
- account_number
- type
- amount

## Database Connection

The database connection is handled in:

```text
database.py
```

Example:

```python
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()
```

## Environment Variables

Create a `.env` file inside the project folder.

Example:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=YOUR_PASSWORD
DB_NAME=bank_system
```

Important: Do not upload the `.env` file to GitHub.

## .gitignore

The `.gitignore` file contains:

```text
.env
__pycache__/
```

This prevents sensitive database credentials and temporary Python files from being uploaded to GitHub.

## Installation

Install the required Python packages:

```bash
pip install mysql-connector-python
pip install python-dotenv
```

## Automated Testing

The project includes automated tests using Python's `unittest` framework.

The test suite contains 12 automated tests covering:

- Customer creation
- Account creation
- Deposits
- Withdrawals
- Transfers
- Account deletion
- Insufficient funds
- Negative deposits
- Negative withdrawals
- Savings account withdrawal limit
- Transfers to the same account
- Transaction persistence in MySQL

The tests use the separate MySQL database:

```text
bank_system_test
```

This prevents automated tests from changing data in the main `bank_system` database.

The test setup also checks that the tests are running only on the test database.

Run the tests with:

```bash
python -m unittest test_bank.py -v
```

Example result:

```text
Ran 12 tests

OK
```

## Example Usage

Create the bank system:

```python
bank = BankAccountSystem()
```

Create a customer:

```python
bank.create_customer(
    1,
    "Max Mustermann",
    "Essen",
    "0123456789",
    "max@example.de"
)
```

Create an account:

```python
bank.create_account(
    "111111",
    1000,
    1
)
```

Deposit money:

```python
bank.deposit(
    "111111",
    200
)
```

Withdraw money:

```python
bank.withdraw(
    "111111",
    100
)
```

Check the balance:

```python
print(
    bank.get_balance("111111")
)
```

Transfer money:

```python
bank.transfer(
    "111111",
    "222222",
    200
)
```

Show all transactions:

```python
bank.show_transactions()
```

Show transactions for one account:

```python
bank.show_account_transactions(
    "111111"
)
```

Show all accounts of one customer:

```python
bank.show_customer_accounts(1)
```

## Savings Account

The project also includes a `SavingsAccount` class.

It inherits from `BankAccountSystem` and overrides the `withdraw()` method.

Example:

```python
savings = SavingsAccount()

savings.withdraw(
    "333333",
    300
)
```

The savings account has a maximum withdrawal limit of:

```text
500 Euro
```

If the user tries to withdraw more than 500 Euro, the operation is rejected.

## Transaction Handling

Transfers use database transaction handling.

If an error occurs during a transfer, the program uses:

```python
connection.rollback()
```

This prevents an incomplete transfer.

For example, money should not be removed from one account without being added to the other account.

## Security

The project includes basic security measures:

- Database password stored in `.env`
- `.env` excluded from GitHub
- Parameterized SQL queries
- Database rollback on failed operations
- Database connection separated from the main program
- Separate test database for automated tests

Example of a parameterized query:

```python
cursor.execute(
    sql,
    (account_number,)
)
```

This is safer than directly inserting user input into an SQL string.

## Error Handling

The program handles several common problems:

- Account already exists
- Customer already exists
- Account does not exist
- Customer does not exist
- Insufficient funds
- Negative deposit
- Negative withdrawal
- Invalid transfer
- Database errors

## Author

Marwan Mohamed

Fachinformatiker für Anwendungsentwicklung