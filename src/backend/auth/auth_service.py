import bcrypt

from mysql.connector import Error, IntegrityError

from src.backend.db.database import get_connection


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
        INSERT INTO users (
            username,
            password_hash,
            role
        )
        VALUES (%s, %s, %s)
        """

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                sql,
                (
                    username,
                    password_hash.decode("utf-8"),
                    role
                )
            )

            connection.commit()

            print("User created successfully.")
            return True

        except IntegrityError:
            if connection:
                connection.rollback()

            print("Username already exists.")
            return False

        except Error as error:
            if connection:
                connection.rollback()

            print("Database error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    def authenticate(self, username, password):
        sql = """
        SELECT
            id,
            username,
            password_hash,
            role
        FROM users
        WHERE username = %s
        """

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                sql,
                (username,)
            )

            user = cursor.fetchone()

            if user is None:
                print("User does not exist.")
                return None

            user_id = user[0]
            db_username = user[1]
            password_hash = user[2]
            role = user[3]

            valid_password = bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8")
            )

            if not valid_password:
                print("Wrong password.")
                return None

            return {
                "id": user_id,
                "username": db_username,
                "role": role
            }

        except Error as error:
            print("Database error:", error)
            return None

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    def login(self, username, password):
        user = self.authenticate(
            username,
            password
        )

        return user is not None