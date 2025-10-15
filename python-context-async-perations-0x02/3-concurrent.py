import sqlite3
import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect("users.db") as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as conn:
        async with conn.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows
    
async def fetch_concurrently():
    rows = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    
    for row in rows:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
