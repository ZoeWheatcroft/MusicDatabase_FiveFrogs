import dbaccess
import useraccess
import songsearch

def play_songID(s_id, user):
    lst = dbaccess.execute_query("SELECT title, length,  song_id, listen_count from SONG where song_id = '%s'" % (s_id))
    print("Playing song", lst[0][0], "for", lst[0][1], "seconds.")
    dbaccess.execute_start("UPDATE song SET listen_count = '%d' WHERE song_id = %s" %  (int(lst[0][3])+1, lst[0][2]))
    lst = dbaccess.execute_query("SELECT * FROM userplayssong WHERE username = '%s' AND song_id = '%s'" % (user, s_id))
    if len(lst) == 0: 
        dbaccess.execute_start("INSERT INTO userplayssong VALUES('%s', '%s', '0')" % (user, s_id))
    lst = dbaccess.execute_query("SELECT * FROM userplayssong WHERE username = '%s' AND song_id = '%s'" % (user, s_id))
    dbaccess.execute_start("UPDATE userplayssong SET play_history = '%d' WHERE song_id = %s AND username = '%s'" %  (int(lst[0][2])+1, lst[0][1], user))

def play_song(user): 
    lst = []
    name = input("Which song would you like to play? ")
    lst = dbaccess.execute_query("SELECT song_id from SONG where title = '%s'" % (name))
    while (len(lst) == 0): 
        name = input("Song name not found! Try again, or enter search to search for songs: ")
        if name.lower() == "search": 
            songsearch.search_screen(user)
            name = input("Which song would you like to play? ")
        
        lst = dbaccess.execute_query("SELECT song_id from SONG where title = '%s'" % (name))
    play_songID(lst[0][0], user)

if __name__ == '__main__': 
    username = useraccess.login()
    play_song(username)