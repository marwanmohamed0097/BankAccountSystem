import bcrypt

from src.backend.db.database import connection, cursor


class AuthService:

    def create_user(self, username, password, role="USER"):
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        sql = """
        INSERT INTO users (username, password_hash, role)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            sql,
            (username, password_hash.decode("utf-8"), role)
        )

        connection.commit()

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