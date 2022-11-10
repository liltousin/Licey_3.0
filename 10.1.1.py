# Импорт библиотеки
import sqlite3

db_name = input()
con = sqlite3.connect(db_name)
cur = con.cursor()

result = cur.execute(
    """
SELECT title FROM films
    WHERE year >= 1997 AND genre IN (
SELECT id FROM genres
    WHERE title IN ('музыка', 'анимация'))
            """
).fetchall()

for elem in result:
    print(elem[0])

con.close()
