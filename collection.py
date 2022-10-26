import dbaccess
import useraccess
import random as r

def create_playlist(username):
    quit = False
    while(not quit):
        name = input("What do you want to name your playlist? ")

        #keeps generating new playlist_id if it already exists in table
        unique_bool = False
        while(not unique_bool):
            random_id = r.randint(1, 99999) 
            playlist_id = int('%i%i' % (30,random_id))
    
            sql_check = "SELECT playlist_id FROM playlist WHERE playlist_id = " + str(playlist_id)
            check_unique = dbaccess.execute_query(sql_check)
            if not check_unique:
                unique_bool = True
    
        insert_playlist = "INSERT into playlist (playlist_id, playlist_name) VALUES('"+ str(playlist_id) + "', '" + name + "');"
        dbaccess.execute_start(insert_playlist)
        insert_creates = "INSERT into usercreatesplaylist (username, playlist_id) VALUES('" + username + "', '" + str(playlist_id) + "');"
        dbaccess.execute_start(insert_creates)

        print("Playlist called '" + name + "' has been made")

        #keep asking if want to create another playlist until valid answer given 
        ans = ""
        while(ans.upper() != "Y" or ans.upper() != "yes"):
            ans = input("Would you like to create another playlist? (Y/N) ")
            if (ans.upper() == "N" or ans.upper() == "no"): 
                quit = True
                break

def view_playlist(username):
    
    show_playlist = "SELECT playlist_id from usercreatesplaylist where username = " + "'" + username + "'"
    user_playlists = dbaccess.execute_query(show_playlist)
    #print(user_playlists)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    if not user_playlists: 
        print("No playlists created")
    else: 
        for playlist in user_playlists: 
            playlist_info = "SELECT p.playlist_name, \
                                (SELECT count(c.song_id) \
                                    FROM playlistcontainssong c \
                                    WHERE p.playlist_id = c.playlist_id) \
                            FROM playlist p \
                                WHERE p.playlist_id = '" + str(playlist[0]) + "'"
            info = dbaccess.execute_query(playlist_info)
            for i in info: 
                print(i)

if __name__ == '__main__': 
    username = useraccess.login()
    #create_playlist(username)
    #create_playlist("hi")
    view_playlist(username)