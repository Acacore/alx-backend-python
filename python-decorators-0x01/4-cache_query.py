import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*conn, query, *args, **kwargs):

        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        

        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print(f"Cache miss. Executed query: {query}")
        return result
    return wrapper
     

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
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")