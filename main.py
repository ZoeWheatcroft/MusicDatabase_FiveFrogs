from PostgresSSH import getCursor, closeDB

cur = getCursor()
cur.execute("SELECT * FROM users")
for x in cur:
    print(x)

cur.execute("INSERT INTO album(album_name, release_date, albumID) values (%s, %s, %s)", ( "Midnights", 10020, "10/20/2022" ))

closeDB()