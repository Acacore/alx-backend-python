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

def stream_users_in_batches(batch_size):
    cur = db_conn.cursor()
    
    cur.execute(f"SELECT * FROM user_data WHERE age > 25 LIMIT {batch_size}")

    for row in cur:
        yield row

def batch_processing(batch_size=25):
    for user in stream_users_in_batches(batch_size):
        print(user)
    

if __name__ == "__main__":
    batch_size=25
    stream_users_in_batches(batch_size)
    batch_processing(batch_size)
    db_conn.close()