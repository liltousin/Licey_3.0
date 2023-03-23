import sqlite3


def get_result(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute(
        '''
    UPDATE Films SET duration = duration * 2
        WHERE genre IN (
    SELECT id FROM Genres WHERE title = "фантастика")'''
    )
    con.commit()
    con.close()
