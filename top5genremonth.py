import dbaccess

def find_top5_genres():
    #top_genres = "SELECT DISTINCT g.genre_name \
                   # FROM songhasgenre g \
                  #  INNER JOIN userplayssong AS s ON (s.song_id == g.song_id) \
                   # ORDER BY "
    top_songs = "SELECT g.genre_name, s.song_id, count(*) listen_total \
                    FROM userplayssong AS s \
                    INNER JOIN songhasgenre AS g ON (s.song_id = g.song_id)\
                    WHERE EXTRACT(MONTH FROM s.play_history) = 11 \
                    AND EXTRACT(YEAR FROM s.play_history) = 2022\
                    GROUP BY s.song_id, g.genre_name \
                    ORDER BY listen_total DESC \
                    LIMIT 5"
    songs_list = dbaccess.execute_query(top_songs)
    print(songs_list)

if __name__ == '__main__': 
    find_top5_genres()
            