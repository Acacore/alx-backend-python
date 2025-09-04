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
USERS = [
    f"user_{i}" for i in range(1, 51)  # 50 sample users
]

def paginate_users(page_size, offset):
    """
    Fetch a page of users starting at `offset` with `page_size` items.
    """
    return USERS[offset: offset + page_size]


def lazy_paginate(page_size):
    """
    Generator that lazily fetches users page by page.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:   # Only ONE loop
        page = paginate_users(page_size, offset)
        if not page:  # No more data
            break
        yield page
        offset += page_size


if __name__ == "__main__":
    for page in lazy_paginate(10):   # page_size = 10
        print(page)
