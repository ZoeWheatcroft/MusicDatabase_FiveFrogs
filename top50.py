import dbaccess
from userfollow import print_list

def top50_header(list_name, dash_len):
    print_list(list_name, dash_len)
    line = "-" * dash_len
    print("%8s | %30s | %25s | %20s" % ("Rank","Song Title", "Artist Name", "Album"))
    print(line)

# Returns the top 50 most popular songs in the last 30 days (rolling)
# TODO: THIS JUST GIVES THE TOP 50 OF ALL TIME, NOT THE PAST 30 DAYS NEEDS FIX (probably will have to add more info to our tables)
def find_top50_recent():
    lst = dbaccess.execute_query("SELECT s.title, a.artist_name, k.album_name \
                                FROM song AS s \
                                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                                INNER JOIN album as k ON (t.album_id = k.album_id) \
                                ORDER BY s.listen_count DESC \
                                LIMIT 50")
    dash_len = 100
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

        print("%8s | %30s | %25s | %20s " % (j, song_title, artist_name, i[2]))
    line = "-" * dash_len
    print(line)

# Returns the top 50 most popular songs among my friends
def find_top50_friends(username):
    lst = dbaccess.execute_query("SELECT s.title, a.artist_name, k.album_name \
                                FROM song AS s \
                                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                                INNER JOIN album as k ON (t.album_id = k.album_id) \
                                INNER JOIN userplayssong as up ON (s.song_id = up.song_id) \
                                INNER JOIN userfollowsuser as u ON (up.username = u.follows) \
                                WHERE u.username = '%s' \
                                ORDER BY s.listen_count DESC \
                                LIMIT 50" % (username))
    dash_len = 100
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

        print("%8s | %30s | %25s | %20s " % (j, song_title, artist_name, i[2]))
    line = "-" * dash_len
    print(line)

if __name__ == '__main__':
    find_top50_friends("chonig41")