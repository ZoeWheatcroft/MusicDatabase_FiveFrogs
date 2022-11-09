from userfollow import print_list
from collection import convert_mins
import useraccess as u
import dbaccess as d

def fyp(username): 
    print_list("Recommended Songs", 10)
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
    AND fp.user_id = '%s' \
    ORDER BY fp.user_id, fp.like_count DESC" % (username))
    for i in lst: 
        duration = convert_mins(i[2])
        print("Song Title: %18s | Artist Name: %14s | Length (sec): %2s" % (i[0], i[1], duration))

if __name__ == '__main__': 
    username = u.login()
    fyp(username)