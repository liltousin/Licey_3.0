import sqlite3


def get_result(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute('''
    DELETE FROM Films
        WHERE genre IN (
    SELECT id FROM Genres WHERE title = "комедия")''')
    con.commit()
    con.close()
