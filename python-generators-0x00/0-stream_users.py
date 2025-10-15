import mysql.connector


# Connect to server
def connect_to_prodev():
    '''Connect diretly to ALX_prodev database'''
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="MySQL@5550100",
        database="ALX_prodev"
    )

#connecting to the prodev database
db_conn = connect_to_prodev()

def stream_users():
    cur = db_conn.cursor()
    cur.execute("SELECT * FROM user_data")

    for row in cur:
        yield row

for user in stream_users():
    print(user)