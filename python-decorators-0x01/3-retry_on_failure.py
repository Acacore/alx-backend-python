import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""
def retry_on_failure(retries, delay):
    def decorator(func):
        @functools.wraps()
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries +1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} falied: {e}")

                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

            
                   
       

def with_db_connection(func):
    """ your code goes here""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
         result = func(conn, cursor, *args, **kwargs)
         conn.commit()
         return result
        finally:
           conn.close()
    return wrapper


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)