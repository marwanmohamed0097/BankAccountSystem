from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.backend.auth.auth_service import AuthService
from src.backend.bank_account_system import BankAccountSystem
from src.backend.db.database import cursor


app = FastAPI()

auth = AuthService()
bank = BankAccountSystem()


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AccountRequest(BaseModel):
    account_number: str
    initial_balance: float = 0
    customer_id: int | None = None


class AmountRequest(BaseModel):
    account_number: str
    amount: float


class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float


@app.get("/")
def home():
    return {
        "message": "Bank Account System API is running"
    }


@app.post("/register")
def register(data: RegisterRequest):

    success = auth.create_user(
        data.username,
        data.password
    )

    if success:
        return {
            "message": "User created successfully"
        }

    return {
        "message": "User could not be created"
    }


@app.post("/login")
def login(data: LoginRequest):

    success = auth.login(
        data.username,
        data.password
    )

    if success:
        return {
            "message": "Login successful"
        }

    return {
        "message": "Invalid username or password"
    }


@app.post("/accounts")
def create_account(data: AccountRequest):

    bank.create_account(
        data.account_number,
        data.initial_balance,
        data.customer_id
    )

    return {
        "message": "Account created"
    }


@app.get("/balance/{account_number}")
def get_balance(account_number: str):

    try:
        balance = bank.get_balance(account_number)

        return {
            "account_number": account_number,
            "balance": balance
        }

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Account does not exist"
        )


@app.post("/deposit")
def deposit(data: AmountRequest):

    bank.deposit(
        data.account_number,
        data.amount
    )

    return {
        "message": "Deposit request completed"
    }


@app.post("/withdraw")
def withdraw(data: AmountRequest):

    bank.withdraw(
        data.account_number,
        data.amount
    )

    return {
        "message": "Withdrawal request completed"
    }


@app.post("/transfer")
def transfer(data: TransferRequest):

    bank.transfer(
        data.from_account,
        data.to_account,
        data.amount
    )

    return {
        "message": "Transfer request completed"
    }


@app.get("/transactions/{account_number}")
def get_transactions(account_number: str):

    cursor.execute(
        """
        SELECT type, amount
        FROM transactions
        WHERE account_number = %s
        """,
        (account_number,)
    )

    transactions = cursor.fetchall()

    return {
        "account_number": account_number,
        "transactions": [
            {
                "type": transaction[0],
                "amount": float(transaction[1])
            }
            for transaction in transactions
        ]
    }


@app.delete("/accounts/{account_number}")
def delete_account(account_number: str):

    bank.delete_account(account_number)

    return {
        "message": "Account deleted"
    }