import sqlite3
import functools

#### decorator to lof SQL queries

import functools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Decorator to log SQL queries
def log_queries():

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Try to extract the SQL query from args or kwargs
            sql = None
            for arg in args:
                if isinstance(arg, str) and arg.strip().lower().startswith(("select", "insert", "update", "delete")):
                    sql = arg
                    break
            if not sql:
                sql = kwargs.get("query", "UNKNOWN SQL")

            logger.info(f"📦 Executing SQL: {sql}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
