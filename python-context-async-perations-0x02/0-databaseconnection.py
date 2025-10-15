import sqlite3

class DatabaseConnection:
    def __init__(self, db_file):
        self.db_file = db_file
       
    def __enter__(self):
        conn = sqlite3.connect(self.db_file)
        conn.cursor()
        self.conn = conn
        return self.conn
    
    def __exit__(self, type, value, traceback):
        self.conn.close()
        

with DatabaseConnection("mydatabase.db") as db_file:
    query = db_file.execute("SELECT * FROM users")
    rows = query.fetchall()
    for row in rows:
        print(row)