import sqlite3

db = sqlite3.connect('main.sqlite')
cursor = db.cursor()
id =cursor.execute(f"SELECT max(user_id) FROM queue WHERE guild_id = 777435243451645983").fetchall()
print (repr(id))