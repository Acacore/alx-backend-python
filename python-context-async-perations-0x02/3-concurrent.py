import sqlite3
import aiosqlite
import asyncio


async def async_fetch_users(db_name):
    async with aiosqlite.connect(db_name) as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(row)


async def async_fetch_older_users(db_name):
    async with aiosqlite.connect(db_name) as conn:
        async with conn.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                print(row)
    
async def fetch_concurrently():
    await asyncio.gather(async_fetch_users("users.db"), async_fetch_older_users("users.db"))

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())



# class ExecuteQuery:
#     def __init__(self, *args, **kwargs):
#         self.db_file = kwargs.get("db_file")
#         self.query = kwargs.get("query")
#         if kwargs.get("age"):
#             self.age = kwargs.get("age")
        
#         def __enter__(self):
#             conn = sqlite3.connect(self.db_file)
#             cursor = conn.cursor()

#             if self.age:
#                 result = cursor.execute(self.query, (self.age,))
#             else:
#                 result = cursor.execute(self.query)
#             self.conn = conn
#             return result.fetchall()
        
#         def __exit__(self, type, value, traceback):
#             self.conn.close()
