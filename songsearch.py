import dbaccess
import useraccess

# search by name
def search_name(username): 
    quit = False
    lst = None
    while(not quit):
        word = input("What is the name of the song that you're searching for? ")
        lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, s.listen_count, k.album_name \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                LEFT JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                WHERE s.title LIKE '%"+word+"%' AND s.song_id = a.song_id \
                ORDER BY s.title, a.artist_name ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Artist Name: %16s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3], i[4]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return lst

def search_artist(username):
    quit = False
    lst = None
    while(not quit): 
        word = input("Who created the song that you're searching for? ")
        lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, s.listen_count, k.album_name \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                LEFT JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                WHERE a.artist_name = '"+ word +"' AND s.song_id = a.song_id \
                ORDER BY s.title, a.artist_name ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Artist Name: %10s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3], i[4]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return lst


def search_album(username): 
    quit = False
    lst = None
    while(not quit): 
        word = input("Which album is the song you're searching for a part of? ")
        lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, s.listen_count, k.album_name \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                LEFT JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                WHERE k.album_name = '"+word+"' AND s.song_id = a.song_id \
                ORDER BY s.title, a.artist_name ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Artist Name: %10s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return lst

def search_genre(username): 
    quit = False
    lst = None
    while(not quit): 
        word = input("Which genre is the song that you're searching for from? ")
        lst = dbaccess.execute_query("SELECT g.genre_name, a.artist_name, s.title, s.length, s.listen_count, k.album_name \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                LEFT JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                LEFT JOIN songhasgenre as g ON (g.song_id = s.song_id) \
                WHERE g.genre_name = '"+word+"' AND s.song_id = a.song_id \
                ORDER BY s.title, a.artist_name ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Genre Name: %10s | Artist Name: %10s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return lst

if __name__ == '__main__': 
    username = useraccess.login()
    search_name(username)
    search_artist(username)
    search_album(username)
    search_genre(username)