from userfollow import print_list
from collection import convert_mins
import useraccess as u
import dbaccess as d

def fyp_header(dash_len):
    list_name = "~*~ Recommended Songs ~*~"
    print_list(list_name, dash_len)
    line = "-" * dash_len
    print("%8s | %30s | %25s | %10s " % ("#", "Song Title", "Artist Name", "Duration"))
    print(line)

def fyp(username): 
    lst = d.execute_query("WITH all_users AS ( \
        SELECT username AS user_id, follows AS friend_id FROM userfollowsuser \
        UNION \
        SELECT follows AS user_id, username AS friend_id FROM userfollowsuser \
    ), friend_plays AS ( \
        SELECT au.user_id, p.song_id, count(p.username) AS like_count \
        FROM all_users AS au \
        LEFT JOIN userplayssong p ON au.friend_id = p.username \
        GROUP BY au.user_id, p.song_id \
    ) \
    SELECT s.title, a.artist_name, s.length \
    FROM friend_plays AS fp \
    LEFT JOIN userplayssong AS p ON fp.user_id = p.username AND fp.song_id = p.song_id \
    INNER JOIN song AS s ON s.song_id = fp.song_id \
    INNER JOIN artistcreatessong AS a ON s.song_id = a.song_id\
    WHERE p.song_id IS null \
    AND fp.user_id = %s \
    ORDER BY fp.user_id, fp.like_count DESC LIMIT 20", (username, ))
    # if no friends, look at play history & songs in genre
    if len(lst) == 0: 
        lst = d.execute_query("WITH userplaysgenre AS (\
        SELECT u.username AS users, g.genre_name AS genre FROM userplayssong u \
        INNER JOIN songhasgenre AS g on u.song_id = g.song_id \
        ), all_songs AS ( \
        SELECT users AS users, genre AS genre FROM userplaysgenre \
        UNION \
        SELECT genre AS users, user AS genre FROM userplaysgenre \
        ), genre_has AS ( \
        SELECT au.users, p.song_id, count(p.genre_name) AS like_count \
        FROM all_songs AS au \
        LEFT JOIN songhasgenre p ON au.genre = p.genre_name \
        GROUP BY au.users, p.song_id \
        ) \
         SELECT s.title, a.artist_name, s.length \
    FROM genre_has AS gh \
    LEFT JOIN userplayssong AS p ON gh.users = p.username AND gh.song_id = p.song_id \
    INNER JOIN song AS s ON s.song_id = gh.song_id \
    INNER JOIN artistcreatessong AS a ON s.song_id = a.song_id\
    WHERE p.song_id IS null \
    AND gh.users = %s \
    ORDER BY gh.users, gh.like_count DESC LIMIT 20", (username, ))
    if( len(lst) == 0 ): 
        print("No play history found! Go play some songs!")

    dash_len = 85
    fyp_header(dash_len)
    line = "-" * dash_len
    print(line)
    j = 0
    for i in lst:
        j += 1
        duration = convert_mins(i[2])
        song_title = i[0]
        if len(song_title) > 30:
            song_title = song_title[:27]
            song_title += "..."
        
        artist_name = i[1]
        if len(artist_name) > 25:
            artist_name = artist_name[:22]
            artist_name += "..."

        print("%8s | %30s | %25s | %10s " % (j, song_title, artist_name, duration))
    line = "-" * dash_len
    print(line)

if __name__ == '__main__': 
    #username = u.login()
    #fyp(username)
    fyp("hannakoh")