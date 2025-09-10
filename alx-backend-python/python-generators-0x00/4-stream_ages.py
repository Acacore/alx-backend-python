import mysql.connector


def connect_to_prodev():
    '''Connect directly to ALX_prodev database'''
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="MySQL@5550100",
        database="ALX_prodev"
    )

db_conn = connect_to_prodev()
def stream_user_ages():
    """
    Generator that yields user ages one by one.
    """
    cur = db_conn.cursor()
    cur.execute("SELECT age FROM user_data")  # fetch only the ages
    for (age,) in cur:   # unpack tuple (since fetch returns tuples)
        yield age
    cur.close()


def calculate_average_age():
    """
    Uses stream_user_ages() to calculate the average age
    without loading the entire dataset into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():   # loop #1
        total += age
        count += 1
    return total / count if count > 0 else 0


if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
    db_conn.close()