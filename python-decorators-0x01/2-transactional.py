import sqlite3 
import functools

"""your code goes here"""
def transactional(func):
    @functools.wraps(func)
    def  wrapper(*args, **kwargs):
       conn = sqlite3.connect('users.db')
       try:
          conn.execute('BEGIN') #start transaction

         # pass the connection into the wrappeed funtion
          result = func(conn, *args, **kwargs)

          conn.commit() # Commit if all is well
          return result
        except as e:
          conn.rollback() # rollaback if error
          print("Action failed", e)
        finally:
          conn.close()

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
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')