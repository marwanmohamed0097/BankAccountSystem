import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


database_name = os.getenv("DB_NAME")

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=database_name
)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = %s
    AND table_name = 'accounts'
    AND column_name = 'user_id'
    """,
    (database_name,)
)

exists = cursor.fetchone()[0]

if not exists:
    cursor.execute(
        """
        ALTER TABLE accounts
        ADD COLUMN user_id INT NULL
        """
    )

connection.commit()

cursor.close()
connection.close()

print("Ownership migration completed")