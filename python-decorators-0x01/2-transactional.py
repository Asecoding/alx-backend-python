import mysql.connector
import functools

# Decorator: Automatically opens and closes DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="ALX_prodev"
            )
            return func(connection, *args, **kwargs)
        finally:
            if connection and connection.is_connected():
                connection.close()
                print("✅ Connection closed.")
    return wrapper

# Decorator: Manages transaction (commit or rollback)
def transactional(func):
    @functools.wraps(func)
    def wrapper(connection, *args, **kwargs):
        try:
            result = func(connection, *args, **kwargs)
            connection.commit()
            print("✅ Transaction committed.")
            return result
        except Exception as e:
            connection.rollback()
            print(f"❌ Transaction rolled back due to error: {e}")
            raise
    return wrapper
