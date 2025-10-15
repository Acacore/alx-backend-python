import mysql.connector
from mysql.connector import errorcode
import csv
import uuid
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, "user_data.csv")
print("CSV file path: ", csv_file)
# Connect to server
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="MySQL@5550100"
        )

# Get a cursor

def create_database(connection):
    '''Create the ALX_prodev database if it does not exist.'''
    cur = connection.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cur.close()


def connect_to_prodev():
    '''Connect diretly to ALX_prodev database'''
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="MySQL@5550100",
        database="ALX_prodev"
    )


# Execute a query
def create_table(connection):
    cur = connection.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),  -- UUID stored as string
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                age DECIMAL(3,0) NOT NULL,     -- age as decimal (integer style)
                INDEX idx_user_id (user_id)
            )
    """)


def insert_data(connection, csv_file):
    '''Insert data from csv into user_data table.'''
    cur = connection.cursor()
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)

        # Skip header row (optional)
        next(reader)
    
    # Loop through rows
        for row in reader:
            cur.execute("""
                INSERT IGNORE INTO user_data(user_id, name, email, age)
                    VALUES(%s, %s, %s, %s)""",
                    (str(uuid.uuid4()), row[0], row[1], row[2]))
            connection.commit() 

if __name__ == "__main__":
    # Step 1: connect to server and ensure DB exists
    server_conn = connect_db()
    create_database(server_conn)
    server_conn.close()

    # Step 2: connect to ALX_prodev database
    db_conn = connect_to_prodev()

    # Step 3: create table
    create_table(db_conn)

    # Step 4: insert data from CSV
    insert_data(db_conn, csv_file)

   
    # Fetch one result
    cur = db_conn.cursor()
    cur.execute("SELECT * FROM user_data LIMIT 1")
    row = cur.fetchone()
    print('First row in DB',row)

    # Close connection
    cur.close()
    db_conn.close()

