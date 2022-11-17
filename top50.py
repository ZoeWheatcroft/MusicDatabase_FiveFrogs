import dbaccess
from userfollow import print_list

def top50_header(list_name, dash_len):
    print_list(list_name, dash_len)
    line = "-" * dash_len
    print("%8s | %30s | %25s | %20s | %10s " % ("Rank","Song Title", "Artist Name", "Album", "Playcount"))
    print(line)

# Returns the top 50 most popular songs in the last 30 days (rolling)
def find_top50_recent():
    lst = dbaccess.execute_query("SELECT s.title, a.artist_name, k.album_name, lc.COUNT \
                                FROM song AS s \
                                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                                INNER JOIN album AS k ON (t.album_id = k.album_id) \
                                INNER JOIN (SELECT song_id, COUNT(*) \
                                            FROM userplayssong AS up \
                                            WHERE up.play_history > (current_date - INTERVAL '30 days') \
                                            GROUP BY song_id) AS lc ON (lc.song_id = s.song_id) \
                                ORDER BY lc.COUNT DESC \
                                LIMIT 50", ())
    dash_len = 120
    list_name = "~*~ Top 50 Charts (Past 30 Days) ~*~"
    top50_header(list_name, dash_len)
    j = 0
    for i in lst:
        j += 1

        song_title = i[0]
        if len(song_title) > 30:
            song_title = song_title[:27]
            song_title += "..."
        
        artist_name = i[1]
        if len(artist_name) > 25:
            artist_name = artist_name[:22]
            artist_name += "..."

        album_name = i[2]
        if len(album_name) > 20:
            album_name = album_name[:17]
            album_name += "..."

        print("%8s | %30s | %25s | %20s | %10s " % (j, song_title, artist_name, album_name, i[3]))
    line = "-" * dash_len
    print(line)

# Returns the top 50 most popular songs among my friends
def find_top50_friends(username):
    lst = dbaccess.execute_query("SELECT s.title, a.artist_name, k.album_name, pc.COUNT \
                                FROM song AS s \
                                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                                INNER JOIN album AS k ON (t.album_id = k.album_id) \
                                INNER JOIN (SELECT song_id, COUNT(*) \
                                            FROM userplayssong AS up \
                                            INNER JOIN userfollowsuser AS uf ON (uf.username = %s) \
                                            WHERE (up.username = uf.follows) \
                                            GROUP BY song_id) AS pc ON (pc.song_id = s.song_id) \
                                ORDER BY pc.COUNT DESC \
                                LIMIT 50", (username, ))
    dash_len = 120
    list_name = "~*~ Top 50 Charts (Among Your Friends) ~*~"
    top50_header(list_name, dash_len)
    j = 0
    for i in lst:
        j += 1

        song_title = i[0]
        if len(song_title) > 30:
            song_title = song_title[:27]
            song_title += "..."
        
        artist_name = i[1]
        if len(artist_name) > 25:
            artist_name = artist_name[:22]
            artist_name += "..."

        album_name = i[2]
        if len(album_name) > 20:
            album_name = album_name[:17]
            album_name += "..."

        print("%8s | %30s | %25s | %20s | %10s " % (j, song_title, artist_name, album_name, i[3]))
    line = "-" * dash_len
    print(line)

if __name__ == '__main__':
    #find_top50_recent()
    find_top50_friends("FiveFrogs11")