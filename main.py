from PostgresSSH import getMyDB, closeDB
conn = getMyDB()
cur = conn.cursor()
cur.execute("SELECT * FROM album")
for x in cur:
    print(x)

#cur.execute("INSERT INTO album(album_name, release_date, albumID) values (%s, %s, %s)", ( "Midnights", 10020, "10/20/2022" ))

closeDB(conn)