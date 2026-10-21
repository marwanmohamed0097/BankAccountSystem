from fastapi import (
    Depends,
    FastAPI,
    HTTPException
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from mysql.connector import Error
from pydantic import BaseModel

from src.backend.auth.auth_service import AuthService
from src.backend.auth.token_service import (
    create_access_token,
    decode_access_token
)

from src.backend.bank_account_system import (
    BankAccountSystem
)

from src.backend.db.database import (
    get_connection
)


app = FastAPI()

auth = AuthService()
bank = BankAccountSystem()

security = HTTPBearer()


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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):
    payload = decode_access_token(
        credentials.credentials
    )

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, role
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User does not exist"
            )

        return {
            "id": user[0],
            "username": user[1],
            "role": user[2]
        }

    except HTTPException:
        raise

    except Error:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    finally:
        if cursor:
            cursor.close()

        if (
            connection
            and connection.is_connected()
        ):
            connection.close()


def require_account_access(
    account_number,
    current_user
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT user_id
            FROM accounts
            WHERE account_number = %s
            """,
            (account_number,)
        )

        account = cursor.fetchone()

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account does not exist"
            )

        if current_user["role"] == "ADMIN":
            return True

        owner_id = account[0]

        if owner_id != current_user["id"]:
            raise HTTPException(
                status_code=403,
                detail=(
                    "You do not have access "
                    "to this account"
                )
            )

        return True

    except HTTPException:
        raise

    except Error:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    finally:
        if cursor:
            cursor.close()

        if (
            connection
            and connection.is_connected()
        ):
            connection.close()


@app.get("/")
def home():
    return {
        "message":
            "Bank Account System API is running"
    }


@app.post("/register")
def register(
    data: RegisterRequest
):
    success = auth.create_user(
        data.username,
        data.password
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="User could not be created"
        )

    return {
        "message":
            "User created successfully"
    }


@app.post("/login")
def login(
    data: LoginRequest
):
    user = auth.authenticate(
        data.username,
        data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid username or password"
            )
        )

    token = create_access_token(
        user["id"],
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/me")
def me(
    current_user: dict = Depends(
        get_current_user
    )
):
    return current_user


@app.post("/accounts")
def create_account(
    data: AccountRequest,
    current_user: dict = Depends(
        get_current_user
    )
):
    success = bank.create_account(
        data.account_number,
        data.initial_balance,
        data.customer_id,
        current_user["id"]
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail=(
                "Account could not be created"
            )
        )

    return {
        "message":
            "Account created successfully",
        "account_number":
            data.account_number
    }


@app.get(
    "/balance/{account_number}"
)
def get_balance(
    account_number: str,
    current_user: dict = Depends(
        get_current_user
    )
):
    require_account_access(
        account_number,
        current_user
    )

    try:
        balance = bank.get_balance(
            account_number
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Account does not exist"
        )

    return {
        "account_number": account_number,
        "balance": balance
    }


@app.post("/deposit")
def deposit(
    data: AmountRequest,
    current_user: dict = Depends(
        get_current_user
    )
):
    require_account_access(
        data.account_number,
        current_user
    )

    success = bank.deposit(
        data.account_number,
        data.amount
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Deposit failed"
        )

    balance = bank.get_balance(
        data.account_number
    )

    return {
        "message": "Deposit successful",
        "account_number":
            data.account_number,
        "balance": balance
    }


@app.post("/withdraw")
def withdraw(
    data: AmountRequest,
    current_user: dict = Depends(
        get_current_user
    )
):
    require_account_access(
        data.account_number,
        current_user
    )

    success = bank.withdraw(
        data.account_number,
        data.amount
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Withdrawal failed"
        )

    balance = bank.get_balance(
        data.account_number
    )

    return {
        "message":
            "Withdrawal successful",
        "account_number":
            data.account_number,
        "balance": balance
    }


@app.post("/transfer")
def transfer(
    data: TransferRequest,
    current_user: dict = Depends(
        get_current_user
    )
):
    require_account_access(
        data.from_account,
        current_user
    )

    success = bank.transfer(
        data.from_account,
        data.to_account,
        data.amount
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Transfer failed"
        )

    return {
        "message":
            "Transfer successful",
        "from_account":
            data.from_account,
        "from_balance":
            bank.get_balance(
                data.from_account
            )
    }


@app.get(
    "/transactions/{account_number}"
)
def get_transactions(
    account_number: str,
    current_user: dict = Depends(
        get_current_user
    )
):
    require_account_access(
        account_number,
        current_user
    )

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                transactions.transaction_type,
                transactions.amount
            FROM transactions
            JOIN accounts
                ON transactions.account_id =
                   accounts.id
            WHERE accounts.account_number = %s
            """,
            (account_number,)
        )

        transactions = cursor.fetchall()

        return {
            "account_number":
                account_number,
            "transactions": [
                {
                    "type":
                        transaction[0],
                    "amount":
                        float(transaction[1])
                }
                for transaction
                in transactions
            ]
        }

    except Error:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

    finally:
        if cursor:
            cursor.close()

        if (
            connection
            and connection.is_connected()
        ):
            connection.close()


@app.delete(
    "/accounts/{account_number}"
)
def delete_account(
    account_number: str,
    current_user: dict = Depends(
        get_current_user
    )
):
    require_account_access(
        account_number,
        current_user
    )

    success = bank.delete_account(
        account_number
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail=(
                "Account could not be deleted"
            )
        )

    return {
        "message":
            "Account deleted successfully",
        "account_number":
            account_number
    }