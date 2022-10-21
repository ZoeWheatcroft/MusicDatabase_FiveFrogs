import PostgresSSH

conn = PostgresSSH.getMyDB()
curs = conn.cursor()

curs.execute("SELECT * FROM album")
for x in curs:
    print(x)

#cur.execute("INSERT INTO album(album_name, release_date, albumID) values (%s, %s, %s)", ( "Midnights", 10020, "10/20/2022" ))

curs.close()
conn.close()