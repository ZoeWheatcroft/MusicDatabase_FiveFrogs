"""
The main function for the playlist is playlist_screen

Access_playlist is called by a wrapper function called see_playlist

All other functions are helper functions for playlist_screen
"""
import dbaccess
import playsong
import useraccess


def print_songs(play_id):
    lst = dbaccess.execute_query("SELECT playlist_name from playlist where playlist_id = '%s'" % (play_id))
    pname = lst[0][0]
    print("Songs in playlist: %s" %(pname))
    lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, k.album_name \
                FROM song AS s \
                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                INNER JOIN album as k ON (t.album_id = k.album_id) \
                INNER JOIN playlistcontainssong as ps ON (ps.song_id = s.song_id) \
                INNER JOIN playlist as p ON (p.playlist_id = ps.playlist_id)\
                WHERE p.playlist_id = '%s' \
                ORDER BY s.title, a.artist_name ASC"%(play_id))
    print("---")
    print("SONGS: ")
    for i in lst:
        print("Artist Name: %16s | Song Title: %18s | Length (sec): %2d | Album Name: %10s " % (i[0], i[1], i[2], i[3]))
    print("---")



"""
Sam's stuff, have not read
"""
def remove_album_from_playlist(playlist_id):
    quit = False
    while(not quit):
        word = input("What is the name of the album that you would like to remove? (or Q to quit): ")
        if word.upper()[0] == "Q":
            break
        # First, find the album with the given name
        album = dbaccess.execute_query("SELECT album_id FROM album WHERE album_name = '%s'"%(word))
        if len(album) > 1:
            # If there are multiple albums with the given name, ask for the artist of the album
            artist = input("Multiple albums found with that name, please specify artist: ")
            album = dbaccess.execute_query("SELECT album_id FROM artistcreatesalbum WHERE artist_name = '%s'"%(artist))
        if len(album) == 1:
            songs = dbaccess.execute_query("SELECT song_id FROM albumcontainssong WHERE album_id = '%s'"%(album[0]))
            # Now remove the songs from the playlist
            if len(songs) != 0:
                quit = True
                for song_id in songs:
                    dbaccess.execute_start("DELETE FROM playlistcontainssong \
                                            WHERE song_id = '%s' \
                                            AND playlist_id = '%s'" 
                                            % (song_id[0], playlist_id))
                print("Songs removed!")
            else:
                print("There are no songs in this album, please try again.")
        elif len(album) == 0:
            print("There is no album with this name, would you like to try again?")
            c = input("[Y] / [N]: ")
            if c.upper()[0] == 'N':
                quit = True

"""
Adds an entire album to a playlist
"""
def add_album_to_playlist(playlist_id):
    quit = False
    while(not quit):
        word = input("What is the name of the album that you would like to add? (or Q to quit): ")
        if word.upper()[0] == "Q":
            break
        # First, find the album with the given name
        album = dbaccess.execute_query("SELECT album_id FROM album WHERE album_name = '%s'"%(word))
        if len(album) > 1:
            # If there are multiple albums with the given name, ask for the artist of the album
            artist = input("Multiple albums found with that name, please specify artist: ")
            album = dbaccess.execute_query("SELECT album_id FROM artistcreatesalbum WHERE artist_name = '%s'"%(artist))
        if len(album) == 1:
            songs = dbaccess.execute_query("SELECT song_id FROM albumcontainssong WHERE album_id = '%s'"%(album[0]))
            # Now add the songs to the playlist
            if len(songs) != 0:
                quit = True
                for song_id in songs:
                    # Insert only songs that do not already exist in the playlist
                    lst = dbaccess.execute_query("SELECT song_id FROM playlistcontainssong \
                                                WHERE song_id = '%s' AND playlist_id = '%s'"
                                                % (song_id[0], playlist_id))
                    if len(lst) == 0:
                        dbaccess.execute_start("INSERT INTO playlistcontainssong (playlist_id, song_id) \
                                                VALUES ('%s', '%s')"
                                                % (playlist_id, song_id[0]))
                print("Songs added!")
            else:
                print("There are no songs in this album, please try again.")
        elif len(album) == 0:
            print("There is no album with this name, would you like to try again?")
            c = input("[Y] / [N]: ")
            if c.upper()[0] == 'N':
                quit = True


"""
asks the user which song on the playlist they'd like to play
gets list of songs with that name and list of songs on playlist 
look for a match and play it
tell the user the song is not on the playlist if there is no match
KNOWN BUGS:
-does not check if either list has length > 0 before iterating through it 
-does not ask user *which* song under that name they mean
"""
def play_song_on_playlist(p_id, user):
    #get the name of the song that's being player
    s_name = input("Which song? ")
    #get list of songs under that name
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

"""
add a song into a playlist
"""
def insert_into_playlist(p_id):
    s_name = input("What's the name of the song you'd like to add? ")
    s_id = dbaccess.execute_query("SELECT song_id FROM song WHERE title = '%s'" % s_name)
    sqlstring = "INSERT into playlistcontainssong (playlist_id, song_id) VALUES('" +  str(p_id) + "', '" + str(s_id[0][0]) + "');"
    dbaccess.execute_start(sqlstring) 
    print("inserted song!")

"""
remove a song from the playlist
"""
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


# Users can sort by song name, artist’s name, genre, and released year
def sort_by_name(play_id): 
    lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, k.album_name \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                LEFT JOIN playlistcontainssong as ps ON (ps.song_id = s.song_id) \
                LEFT JOIN playlist as p ON (p.playlist_id = ps.playlist_id)\
                WHERE p.playlist_id = '%s' \
                GROUP BY a.artist_name, s.title, s.length, k.album_name \
                ORDER BY s.title ASC"%(play_id))
    print("---")
    print("SONGS: ")
    for i in lst:
        print("Artist Name: %16s | Song Title: %18s | Length (sec): %2d | Album Name: %10s " % (i[0], i[1], i[2], i[3]))
    print("---")

def sort_by_artist(play_id): 
    lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, k.album_name \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                LEFT JOIN playlistcontainssong as ps ON (ps.song_id = s.song_id) \
                LEFT JOIN playlist as p ON (p.playlist_id = ps.playlist_id)\
                WHERE p.playlist_id = '%s' \
                GROUP BY a.artist_name, s.title, s.length, k.album_name\
                ORDER BY a.artist_name ASC"%(play_id))
    print("---")
    print("SONGS: ")
    for i in lst:
        print("Artist Name: %16s | Song Title: %18s | Length (sec): %2d | Album Name: %10s " % (i[0], i[1], i[2], i[3]))
    print("---")

def sort_by_genre(play_id): 
    lst = dbaccess.execute_query("SELECT s.song_id, g.genre_name, a.artist_name, s.title, s.length, k.album_name \
                FROM song AS s \
                INNER JOIN artistcreatessong AS a ON(s.song_id = a.song_id)  \
                INNER JOIN playlistcontainssong as ps ON (ps.song_id = s.song_id) \
                LEFT JOIN playlist as p ON (p.playlist_id = ps.playlist_id AND p.playlist_id = ps.playlist_id)\
                LEFT JOIN songhasgenre as g ON (g.song_id = s.song_id AND g.song_id = ps.song_id ) \
                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                WHERE p.playlist_id = '%s' \
                GROUP BY s.song_id, g.genre_name, a.artist_name, s.title, s.length, k.album_name\
                ORDER BY g.genre_name ASC"%(play_id))
    print("---")
    print("SONGS: ")
    for i in lst:
        print("%s Genre Name: %6s | Artist Name: %16s | Song Title: %18s | Length (sec): %2d | Album Name: %10s " % (i[0], i[1], i[2], i[3], i[4], i[5]))
    print("---")

def sort_by_month(play_id): 
    lst = dbaccess.execute_query("SELECT a.artist_name, s.title, s.length, k.album_name, EXTRACT(MONTH from s.song_release_date) AS month \
                FROM song AS s \
                LEFT JOIN artistcreatessong AS a ON(s.song_id = a.song_id) \
                INNER JOIN artistcreatesalbum AS t ON (a.artist_name = t.artist_name) \
                LEFT JOIN album as k ON (t.album_id = k.album_id) \
                INNER JOIN playlistcontainssong as ps ON (ps.song_id = s.song_id) \
                LEFT JOIN playlist as p ON (p.playlist_id = ps.playlist_id)\
                WHERE p.playlist_id = '%s' \
                GROUP BY a.artist_name, s.title, s.length, k.album_name, s.song_release_date \
                ORDER BY month ASC"%(play_id))
    print("---")
    print("SONGS: ")
    for i in lst:
        print("Artist Name: %16s | Song Title: %18s | Length (sec): %2d | Album Name: %10s | Month: %s" % (i[0], i[1], i[2], i[3], i[4]))
    print("---")


def sort_playlist(playlist_id): 
    inp = input("Sort songs by [1] Song name, [2] Artist name, [3] Genre, [4] Released month ")
    if(inp == "1"):
        sort_by_name(playlist_id)
    elif(inp == "2"): 
        sort_by_artist(playlist_id)
    elif(inp == "3"): 
        sort_by_genre(playlist_id)
    elif(inp == "4"): 
        sort_by_month(playlist_id)
    else: 
        print("invalid input")
    

"""
Wrapper function for access_playlist
Asks which playlist to open and then accesses it w/ access_playlist
Uses name of playlist to get first playlist under that name 
KNOWN BUGS: 
-no check to see if there are multiple playlists under that name
"""
def see_playlist(user):
    inp = input("What's the name of the playlist? ")
    # This sql statement checks if the playlist belongs to a user, and whether the playlist even exists.
    lst = dbaccess.execute_query("SELECT p.playlist_id FROM playlist AS p \
        LEFT JOIN usercreatesplaylist AS u ON (u.playlist_id = p.playlist_id)\
        WHERE p.playlist_name = '%s' AND u.username = '%s'" % (inp, user))
    #should do a check here to see if there's multiple under same name
    # This if checks if the sql statement gets anything. 
    if len(lst) == 1:
        playlist_screen(user, int(str(lst[0][0])))
    else: 
        print("Playlist not found!")
            

"""
print options of actions on playlist
UPDATE IF OPTIONS CHANGE
"""
def print_options():
    print("")
    print("0 - List songs")
    print("1 - Play song")
    print("2 - Play entire playlist")
    print("3 - Sort playlist")
    print("4 - Add song")
    print("5 - Delete song")
    print("6 - Add album")
    print("7 - Delete album")
    print("8 - Exit")
"""
main function 
"""
def playlist_screen(user, playlist_id): 
    #get the playlist name 
    print_songs(playlist_id)
    print_options()
    num = input("Enter your selection here: ")
    #get player actions and perform while valid = true
    valid = False
    while not valid:
        #print out the songs
        if num == "0":
            print_songs(playlist_id)
        #play song
        elif num == "1": 
            valid = True
            play_song_on_playlist(playlist_id, user)
        #sort by 
        elif num == "2":
            valid = True
            playsong.play_playlistbyid(playlist_id)
        elif num == "3": 
            valid = True
            sort_playlist(playlist_id)
        #add a song to the playlist
        elif num == "4":
            valid = True
            insert_into_playlist(playlist_id)
        #delete a song from the playlist
        elif num == "5": 
            valid = True
            remove_song_from_playlist(playlist_id, user)   
        #exit
        elif num == "6":
            valid = True
            add_album_to_playlist(playlist_id)
        elif num == "7":
            remove_album_from_playlist(playlist_id)
        elif num == "8":
            return 0
        elif num == "h" or num == "H":
            print_options()
        #got bad input
        else: 
            print("Incorrect input, please retry")
        #get input for next round if not exiting 9THIS NEEDS TO BE ANOTHER WHILE)
        if(num != "5"):
            num = input("(h for options) Enter your selection here: ")

if __name__ == '__main__': 
    user = useraccess.login()
    see_playlist(user)
    