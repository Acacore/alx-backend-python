import sqlite3

class ExecuteQuery:
    def __init__(self, db_file, query, age):
        self.db_file = db_file
        self.query = query
        self.age = age
       
    def __enter__(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        result = cursor.execute(self.query, self.age,)
        rows = result.fetchall()
        self.conn = conn
        return rows
    
    def __exit__(self, type, value, traceback):
        self.conn.close()
        

with ExecuteQuery("mydatabase.db", "SELECT * FROM users WHERE age > ?", (25,) ) as db_file:
    for row in db_file:
        print(row)