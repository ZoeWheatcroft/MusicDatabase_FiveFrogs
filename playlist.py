import dbaccess
import useraccess
import songsearch
import playsong


def print_songs(songs):
    print("---")
    print("SONGS: ")
    for song in songs:
        print("| ", song[0])
        song_name = dbaccess.execute_query("SELECT title FROM song where song_id ='%s'" % song)
        print(song_name[0][0])
    print("---")

def play_playlist(user):
    inp = input("What's the name of the playlist? ")
    lst = dbaccess.execute_query("SELECT playlist_id FROM playlist WHERE playlist_name = '%s'" % (inp))
    print(lst)
    access_playlist(user, int(str(lst[0][0])))

def remove_album_from_playlist(playlist_id):
    quit = False
    while(not quit):
        word = input("What is the name of the album that you would like to remove? ")
        # First, find the album with the given name
        album = dbaccess.execute_query("SELECT album_id FROM album WHERE album_name = '%s'"%(word))
        if len(album) == 1:
            songs = dbaccess.execute_query("SELECT song_id FROM albumcontainssong WHERE album_id = '%s'"%(album))
            # Now remove the songs from the playlist
            if len(songs) != 0:
                quit = True
                for s in songs:
                    dbaccess.execute_start("DELETE FROM playlistcontainssong WHERE song_id = '"+ s +"' AND playlist_id = '"+ playlist_id +"'")
            else:
                print("There are no songs in the playlist from this album, please try again")
        elif len(album) == 0:
            print("There is no album with this name, would you like to try again?")
            c = input("[Y] / [N]")
            if c.upper()[0] == 'N':
                quit = True


def access_playlist(user, playlist_id): 
    #get the playlist name 
    lst = dbaccess.execute_query("SELECT playlist_name from playlist where playlist_id = '%s'" % (playlist_id))
    pname = lst[0]
    songs = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%s'" % playlist_id)
    print_songs(songs)
    print('currently accessing playlist: ', pname)
    print("")
    print("0 - list songs")
    print("1- play song")
    print("2- sort by...")
    print("3- add song")
    print("4- delete song")
    print("5- exit")
    num = input("Enter your selection here: ")
    valid = False
    while not valid:
        #print out the songs
        if num == "0":
            songs = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%s'" % playlist_id)
            print_songs(songs)
        #play song
        elif num == "1": 
            valid = False
            s_id = input("Which song?")
            #check that song is in the play list
            lst = []
            lst = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%s'" % playlist_id)
            song_in_playlist = False
            #I wassss doing a check to see if the song was actually in the play list but it's not working and i got other stuff to do
            #will come back if i have time
            """
            for song in lst:
                if(song == s_id):
                    print(song)
                    song_in_playlist = True
            if(song_in_playlist):
                playsong.play_songID(s_id, user)
            else:
                print("Sorry, that song isn't in your playlist!")
            """
            playsong.play_songID(s_id, user)
        #sort by 
        elif num == "2": 
            inp = input("Sort songs (1)ascendingly or (2)descendingly? (1, 2) ")
            if(inp == "1"):
                songs = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%d' ORDER BY song_id ASC" % playlist_id)
            
            else:
                songs = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%d' ORDER BY song_id DESC" % playlist_id)
            
            print_songs(songs)
            valid = False
        #add a song to the playlist
        elif num == "3":
            s_id = input("What's the id of the song you'd like to add? ")
            playlist_id_str = str(playlist_id)
            sqlstring = "INSERT into playlistcontainssong (playlist_id, song_id) VALUES('" +  playlist_id_str + "', '" + s_id + "');"
            dbaccess.execute_start(sqlstring) 
            print("inserted song!")
            valid = False
        #delete a song from the playlist
        elif num == "4": 
            inp = input("What's the id of the song you'd like to remove? ")
            dbaccess.execute_start("DELETE FROM playlistcontainssong WHERE song_id = '%d'" % int(inp))
            valid = False
        #exit
        elif num == "5":
            valid = True
        #got bad input
        else: 
            num = input("Incorrect value. Please try again: [1, 2, 3, 4, 5] ")
        #get input for next round if not exiting
        if(num != "5"):
            num = input("Enter your selection here: ")

    #name = input("Which song would you like to play? ")
    #lst = dbaccess.execute_query("SELECT song_id from SONG where title = '%s'" % (name))
    #while (len(lst) == 0): 
    #    name = input("Song name not found! Try again, or enter search to search for songs: ")
    #    if name.lower() == "search": 
    #        songsearch.search_screen(user)
    #        name = input("Which song would you like to play? ")
        
    #    lst = dbaccess.execute_query("SELECT song_id from SONG where title = '%s'" % (name))
    #play_songID(lst[0][0], user)

if __name__ == '__main__': 
    play_playlist("celery")
    