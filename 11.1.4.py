import sqlite3


def get_result(name):
    con = sqlite3.connect(name)
    cur = con.cursor()
    cur.execute(
        '''
    DELETE FROM Films
        WHERE title LIKE "Я%а"'''
    )
    con.commit()
    con.close()
