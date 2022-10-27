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
    #check if user has any playlists or not 
    show_playlist = "SELECT playlist_id from usercreatesplaylist where username = " + "'" + username + "'"
    user_playlists = dbaccess.execute_query(show_playlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if not user_playlists: 
        print("No playlists created")
    else: 
        playlist_info = "SELECT p.playlist_name, COUNT(c.song_id), SUM(s.length)\
                            FROM playlist AS p \
                            LEFT JOIN playlistcontainssong AS c ON (p.playlist_id = c.playlist_id)\
                            LEFT JOIN song AS s ON (s.song_id = c.song_id)\
                            LEFT JOIN usercreatesplaylist AS u on (p.playlist_id = u.playlist_id) \
                            WHERE u.username = '" + username + "'" +\
                            "GROUP BY p.playlist_id \
                            ORDER BY p.playlist_name ASC"

        all_playlists = dbaccess.execute_query(playlist_info)
        for playlist in all_playlists: 
            print(playlist)

if __name__ == '__main__': 
    username = useraccess.login()
    #create_playlist(username)
    #create_playlist("hi")
    view_playlist(username)
    #view_playlist("lh5844")