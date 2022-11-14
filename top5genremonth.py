import dbaccess
import datetime 
from userfollow import print_list


def top5_header(dash_len, curr):
    list_name = "~*~ Top 5 Genres in %s ~*~" % (curr.strftime("%B"))
    print_list(list_name, dash_len)
    line = "-" * dash_len
    print("%5s | %3s" % ("Rank","Genre"))
    print(line)

def find_top5_genres():
    curr = datetime.datetime.now()
    curr_month = curr.month
    curr_year = curr.year

    top_songs = "SELECT g.genre_name, s.song_id, count(*) listen_total \
                    FROM userplayssong AS s \
                    INNER JOIN songhasgenre AS g ON (s.song_id = g.song_id)\
                    WHERE EXTRACT(MONTH FROM s.play_history) = %d\
                    AND EXTRACT(YEAR FROM s.play_history) = %d\
                    GROUP BY s.song_id, g.genre_name \
                    ORDER BY listen_total DESC \
                    LIMIT 5" % (curr_month, curr_year)
    songs_list = dbaccess.execute_query(top_songs)

    dash_len = 40
    top5_header(dash_len, curr)
    rank = 0
    for song in songs_list:
        rank += 1
        print("%5s | %3s" % (rank, song[0]))

    line = "-" * dash_len
    print(line)

if __name__ == '__main__': 
    find_top5_genres()
            