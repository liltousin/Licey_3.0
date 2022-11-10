import sqlite3

db_name = input()
con = sqlite3.connect(db_name)
cur = con.cursor()

result = cur.execute(
    """
SELECT title FROM Films
    WHERE duration >= 60 AND genre=(
SELECT id FROM genres
    WHERE title = 'комедия')
            """
).fetchall()

for elem in result:
    print(elem[0])

con.close()
