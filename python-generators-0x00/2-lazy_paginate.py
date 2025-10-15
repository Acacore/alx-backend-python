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
# Simulated data source (e.g., users in a DB)
def paginate_users(page_size, offset):
    """
    Fetch a page of users from user_data table.
    Uses LIMIT and OFFSET to fetch a slice of rows.
    """
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)  # dictionary=True returns dict rows
    cursor.execute(
        "SELECT * FROM user_data LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of users from DB.
    Uses only ONE loop and yields one page at a time.
    """
    offset = 0
    while True:  # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    for page in lazy_paginate(5):  # page_size = 5
        print(page)
