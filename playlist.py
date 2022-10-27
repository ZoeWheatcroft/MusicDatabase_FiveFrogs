from turtle import pos
import dbaccess
import useraccess
import songsearch
import playsong


def print_songs(songs):
    print("---")
    print("SONGS: ")
    for song in songs:
        song_name = dbaccess.execute_query("SELECT title FROM song where song_id ='%s'" % song)
        print("| ", song_name[0][0])
        print("|    -", song[0])
    print("---")

"""
Wrapper function for access_playlist
Asks which playlist they're accessing 
"""
def play_playlist(user):
    inp = input("What's the name of the playlist? ")
    lst = dbaccess.execute_query("SELECT playlist_id FROM playlist WHERE playlist_name = '%s'" % (inp))
    #should do a check here to see if there's multiple under same name
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

def play_song_on_playlist(p_id, user):
    #get the name of the song that's being player
    s_name = input("Which song? ")
    #in the case that there's multiple songs on a playlist under the same name, we'll just play the first result
    lst_possible_matches = dbaccess.execute_query("SELECT song_id FROM song WHERE title = '%s'" % s_name)
    #check that song is in the play list
    lst_songsinplaylist = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%s'" % p_id)
    song_in_playlist = False
    s_id_found= 0
    for id in lst_songsinplaylist:
        for pmatch in lst_possible_matches:
            if(id[0] == pmatch[0]):
                song_in_playlist = True
                s_id_found = id[0]
    if(song_in_playlist):
        playsong.play_songID(s_id_found, user)
    else:
        print("Sorry, that song isn't in your playlist!")
    #playsong.play_songID(s_id, user)

def insert_into_playlist(p_id):
    s_name = input("What's the name of the song you'd like to add? ")
    s_id = dbaccess.execute_query("SELECT song_id FROM song WHERE title = '%s'" % s_name)
    sqlstring = "INSERT into playlistcontainssong (playlist_id, song_id) VALUES('" +  str(p_id) + "', '" + str(s_id[0][0]) + "');"
    dbaccess.execute_start(sqlstring) 
    print("inserted song!")

def remove_song_from_playlist(p_id, user):
    inp = input("What's the name of the song you'd like to remove? ")
    possible_matches = dbaccess.execute_query("SELECT song_id FROM song WHERE title = '%s'" % inp)
    if(len(possible_matches) == 0):
        print("That's not a song, sorry! ")
        return 0
    else:
        print("removing song: '%s' ..." % inp)
        #get a list of every song in the playlist
        playlist_songs = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong where playlist_id = '%s'" % p_id)
        #check if any of the possible matches are also on the list
        for s in playlist_songs:
            for p in possible_matches:
                if(p[0] == s[0]):
                    dbaccess.execute_start("DELETE FROM playlistcontainssong WHERE song_id = '%s'" % str(p[0]))
    
def print_options():
    print("")
    print("0- list songs")
    print("1- play song")
    print("2- sort by...")
    print("3- add song")
    print("4- delete song")
    print("5- exit")

def access_playlist(user, playlist_id): 
    #get the playlist name 
    lst = dbaccess.execute_query("SELECT playlist_name from playlist where playlist_id = '%s'" % (playlist_id))
    pname = lst[0]
    songs = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong WHERE playlist_id = '%s'" % playlist_id)
    print_songs(songs)
    print('currently accessing playlist: ', pname)
    print_options()
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
            play_song_on_playlist(playlist_id, user)
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
            insert_into_playlist(playlist_id)
            valid = False
        #delete a song from the playlist
        elif num == "4": 
            remove_song_from_playlist(playlist_id, user)
            valid = False
        #exit
        elif num == "5":
            valid = True
        elif num == "h" or num == "H":
            print_options()
            valid = False
        #got bad input
        else: 
            valid = False
            print("Incorrect input, please retry")
        #get input for next round if not exiting
        if(num != "5"):
            num = input("(h for options) Enter your selection here: ")

if __name__ == '__main__': 
    play_playlist("celery")
    