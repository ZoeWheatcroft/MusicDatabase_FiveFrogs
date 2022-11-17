import dbaccess
import useraccess
import songsearch
import collection as c
import datetime as d
import useraccess as u

def play_songID(s_id, user):
    lst = dbaccess.execute_query("SELECT title, length, song_id, listen_count from SONG where song_id = %s", (s_id, ))
    duration = c.convert_mins(lst[0][1])
    print("Playing song '%s' for" % (lst[0][0]), duration)
    dbaccess.execute_start("UPDATE song SET listen_count = %s WHERE song_id = %s", (int(lst[0][3])+1, lst[0][2]))
    dbaccess.execute_start("INSERT INTO userplayssong VALUES(%s, %s, %s)", (user, s_id, d.datetime.now()))

def play_song(user): 
    quit = False
    while(not quit): 
        lst = []
        name = input("Which song would you like to play? ")
        lst = dbaccess.execute_query("SELECT s.song_id, s.title, a.artist_name from SONG AS s \
            INNER JOIN artistcreatessong AS a ON (s.song_id = a.song_id) where s.title = %s", (name, ))
        while (len(lst) == 0): 
            name = input("Song name not found! Try again, or enter search to search for songs, or quit to quit: ")
            if name.lower() == "search": 
                songsearch.search_screen(user)
                name = input("Which song would you like to play? ")
            if name.lower() == "quit": 
                return 0
            lst = dbaccess.execute_query("SELECT s.song_id, s.title, a.artist_name from SONG AS s \
            INNER JOIN artistcreatessong AS a ON (s.song_id = a.song_id) where s.title = %s", (name, ))
        if (len(lst) > 1): 
            print("Multiple songs found!")
            for i in lst: 
                print("Artist Name: %16s | Song Title: %18s | %s" % (i[2], i[1], i[0]))
            artist = input("Who is this song by? ")
            lst = dbaccess.execute_query("SELECT s.song_id, s.title, a.artist_name from SONG AS s \
            INNER JOIN artistcreatessong AS a ON (s.song_id = a.song_id) where s.title = %s AND a.artist_name = %s", (name, artist))
        while(len(lst) == 0): 
            artist = input("Song by this artist not found! Enter the artist name again, or enter search to search for songs, or quit to quit: ")
            if artist.lower() == "search": 
                songsearch.search_screen(user)
                artist = input("Who is this song by? ")
            if artist.lower() == "quit": 
                return 0
            lst = dbaccess.execute_query("SELECT s.song_id, s.title, a.artist_name from SONG AS s \
            INNER JOIN artistcreatessong AS a ON (s.song_id = a.song_id) where s.title = %s AND a.artist_name = %s", (name, artist))
        play_songID(lst[0][0], user)
        quit = u.keep_asking("Would you like to play another song? ")


def play_playlistbyid(user, play_id): 
    # select all songs in the playlist
    lst = dbaccess.execute_query("SELECT s.song_id \
                FROM song AS s \
                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                INNER JOIN playlistcontainssong as ps ON (ps.song_id = s.song_id) \
                WHERE ps.playlist_id = %s \
                ORDER BY s.title, a.artist_name ASC", (play_id, ))
    for i in lst: 
        play_songID(i[0], user)

if __name__ == '__main__': 
    username = useraccess.login()
    play_song(username)