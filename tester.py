import sqlite3

db = sqlite3.connect('main.sqlite')
cursor = db.cursor()
playerQuery = cursor.execute(f"SELECT user_id FROM queue").fetchall()
playerList = ""
for row in playerQuery:
        playerList += "".join(row) + "\n"
print(playerList)