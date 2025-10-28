import aiosqlite, pathlib
DB = pathlib.Path("bot.db")

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(id INTEGER PRIMARY KEY, stars INTEGER DEFAULT 0, ref INTEGER DEFAULT 0)"
        )
        await db.commit()

async def add_stars(uid: int, amount: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO users(id,stars) VALUES(?,?) ON CONFLICT(id) "
            "DO UPDATE SET stars=stars+?",
            (uid, amount, amount)
        )
        await db.commit()

async def get_stars(uid: int) -> int:
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT stars FROM users WHERE id=?", (uid,))
        row = await cur.fetchone()
        return row[0] if row else 0

async def add_ref(uid: int, ref_id: int):
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET ref=ref+1 WHERE id=?", (ref_id,))
        await db.execute(
            "INSERT INTO users(id,stars) VALUES(?,10) ON CONFLICT(id) "
            "DO UPDATE SET stars=stars+10",
            (uid,)
        )
        await db.commit()