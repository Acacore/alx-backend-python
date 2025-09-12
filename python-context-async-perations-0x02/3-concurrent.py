import sqlite3
import aiosqlite
import asyncio


async def async_fetch_users(db_name):
    conn =  await aiosqlite.connect(db_name)
    conn.cursor()
    query = await conn.execute("SELECT * FROM users")
    rows = await query.fetchall()
    for row in rows:
        print(row)


async def async_fetch_older_users(db_name):
    conn =  await aiosqlite.connect(db_name)
    conn.cursor()
    query = await conn.execute("SELECT * FROM users WHERE age > 40")
    rows = await query.fetchall()
    for row in rows:
        print(row)
    
async def main():
    await asyncio.gather(async_fetch_users("users.db"), async_fetch_older_users("users.db"))

asyncio.run(main())



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
