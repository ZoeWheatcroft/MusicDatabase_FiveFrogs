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
                print("Artist Name: %14s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3], i[4]))
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
                print("Genre Name: %6s | Artist Name: %14s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3], i[4], i[5]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return lst

def search_screen(username): 
    print("How would you like to search for a song? ")
    print("1. By name")
    print("2. By artist")
    print("3. By album")
    print("4. By genre")
    num = input("Enter your selection here: [1, 2, 3, 4] ")
    valid = False
    while not valid:
        if num == "1": 
            valid = True
            search_name(username)
        elif num == "2": 
            valid = True
            search_artist(username)
        elif num == "3": 
            valid = True
            search_album(username)
        elif num == "4": 
            valid = True
            search_genre(username)
        else: 
            num = input("Incorrect value. Please try again: [1, 2, 3, 4] ")


if __name__ == '__main__': 
    username = useraccess.login()
    search_screen(username)