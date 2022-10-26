import dbaccess
import useraccess

# search by name
def search_name(username): 
    quit = False
    while(not quit):
        word = input("What is the name of the song that you're searching for? ")
        lst = dbaccess.execute_query("SELECT title, length, listen_count from song WHERE title LIKE '%" + word + "%' ORDER BY title ASC" )
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Song Title: %18s | Length (sec): %2d | Number of plays: %3d" % (i[0], i[1], i[2]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return None

def search_artist(username):
    quit = False
    while(not quit): 
        word = input("Who created the song that you're searching for? ")
        lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, s.listen_count, t.album name FROM song AS s, JOIN artistcreatessong AS a ON(s.song_id = a.song_id) JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) WHERE artist_name = '" + word + "' AND s.song_id = a.song_id ORDER BY title ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Artist Name: %10s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d | Album Name: %10s " % (i[0], i[1], i[2], i[3], i[4]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True


def search_album(username): 
    quit = False
    while(not quit): 
        word = input("Which album is the song you're searching for a part of? ")
        lst = dbaccess.execute_query("SELECT a.album_name, s.title, s.length, s.listen_count FROM song s, albumcontainssong a WHERE a.album_name = '" + word + "' AND s.song_id = a.song_id ORDER BY title ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Album Name: %10s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d" % (i[0], i[1], i[2], i[3]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True

def search_genre(username): 
    quit = False
    while(not quit): 
        word = input("Which genre is the song that you're searching for from? ")
        lst = dbaccess.execute_query("SELECT g.genre_name, s.title, s.length, s.listen_count FROM song s, songhasgenre g WHERE g.genre_name = '" + word + "' AND s.song_id = g.song_id ORDER BY title ASC")
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Genre Name: %10s | Song Title: %18s | Length (sec): %2d | Number of plays: %3d" % (i[0], i[1], i[2], i[3]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True

if __name__ == '__main__': 
    #username = useraccess.login()
    search_artist("hi")