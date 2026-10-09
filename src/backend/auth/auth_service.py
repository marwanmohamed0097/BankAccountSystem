import bcrypt

from mysql.connector import Error, IntegrityError
from src.backend.db.database import connection, cursor


class AuthService:

    def create_user(self, username, password):
        role = "USER"

        if not username or len(username) < 3:
            print("Username must be at least 3 characters.")
            return False

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return False

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        sql = """
        INSERT INTO users (username, password_hash, role)
        VALUES (%s, %s, %s)
        """

        try:
            cursor.execute(
                sql,
                (username, password_hash.decode("utf-8"), role)
            )

            connection.commit()

            print("User created successfully.")
            return True

        except IntegrityError:
            connection.rollback()
            print("Username already exists.")
            return False

        except Error as error:
            connection.rollback()
            print("Database error:", error)
            return False

    def login(self, username, password):
        sql = """
        SELECT password_hash, role
        FROM users
        WHERE username = %s
        """

        cursor.execute(
            sql,
            (username,)
        )

        user = cursor.fetchone()

        if user is None:
            print("User does not exist.")
            return False

        password_hash = user[0]
        role = user[1]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        ):
            print("Login successful.")
            print("Role:", role)
            return True

        print("Wrong password.")
        return False