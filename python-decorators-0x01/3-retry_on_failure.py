import time
import sqlite3
import functools


def retry_on_failure(retries=3, delay=2):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"⏳ Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("❌ All retry attempts failed.")
                        raise

        return wrapper

    return decorator
