import sqlite3

artist_name = input()
con = sqlite3.connect('music_db.sqlite')
cur = con.cursor()

result = cur.execute(
    """
SELECT DISTINCT
    Track.Name
FROM
    Track
LEFT JOIN Album ON Album.AlbumId == Track.AlbumId
LEFT JOIN Artist ON Artist.ArtistId == Album.ArtistId
WHERE
    Artist.Name = ?
            """, (artist_name, )
).fetchall()

for elem in sorted(result, key=lambda x: x[0]):
    print(elem[0])

con.close()
