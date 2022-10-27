from ast import Break
import dbaccess
import useraccess
import random as r
import datetime

def create_playlist(username):
    quit = False
    while(not quit):
        name = input("What do you want to name your new playlist? ")

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
        while(True):
            ans = input("Would you like to create another playlist? (Y/N) ")
            if (ans.upper() == "Y" or ans.upper() == "YES"): 
                break
            if (ans.upper() == "N" or ans.upper() == "NO"): 
                quit = True
                break

def convert_mins(secs):
    if secs == None: 
        return "0:00:00"
    duration = str(datetime.timedelta(seconds=secs))
    return duration

def view_playlist(username):
    #check if user has any playlists or not 
    show_playlist = "SELECT playlist_id from usercreatesplaylist where username = '%s'" % (username)
    user_playlists = dbaccess.execute_query(show_playlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if not user_playlists: 
        print("No playlists created")
        return None
    else: 
        playlist_info = "SELECT p.playlist_name, COUNT(c.song_id), SUM(s.length), p.playlist_id\
                            FROM playlist AS p \
                            LEFT JOIN playlistcontainssong AS c ON (p.playlist_id = c.playlist_id)\
                            LEFT JOIN song AS s ON (s.song_id = c.song_id)\
                            LEFT JOIN usercreatesplaylist AS u on (p.playlist_id = u.playlist_id) \
                            WHERE u.username = '" + username + "'" +\
                            "GROUP BY p.playlist_id \
                            ORDER BY p.playlist_name ASC"

        all_playlists = dbaccess.execute_query(playlist_info)
        print("%11s ~*~ Your Playlists ~*~" % (" "))
        print("-----------------------------------------------")
        print("%16s | %15s | %8s" % ("Playlist Name", "Number of Songs", "Duration"))
        print("-----------------------------------------------")
        for playlist in all_playlists: 
            duration = convert_mins(playlist[2])
            print("%16s | %9s songs | %8s" % (playlist[0], playlist[1], duration))
            print(playlist[3])
        return all_playlists

def rename_playlist(username, all_playlists):
    if all_playlists == None: 
        print("Error: No playlists available to rename")
    else: 
        quit = False
        while(not quit):
            rename = input("Which playlist do you want to rename? ")
            #check if that playlist name exists 
            if rename not in all_playlists[0]:
                print("Error: '%s' does not exist" % (rename))
            else: 
                name = input("What do you want to name it to? ")
                select_rename_id = "SELECT p.playlist_id \
                            FROM playlist AS p \
                            LEFT JOIN usercreatesplaylist AS u on (p.playlist_id = u.playlist_id) \
                            WHERE u.username = '%s' AND p.playlist_name = '%s'" % (username, rename)
                rename_id = dbaccess.execute_query(select_rename_id)
                print(rename_id[0][0])
                dbaccess.execute_start("UPDATE playlist SET playlist_name = '%s' \
                                        WHERE playlist_id = '%s'" % (name, rename_id[0][0]))

                print("'%s' renamed to '%s'" % (rename, name))

            #keep asking if want to rename another playlist until valid answer given 
            while(True):
                ans = input("Would you like to rename another playlist? (Y/N) ")
                if (ans.upper() == "Y" or ans.upper() == "YES"): 
                    break
                if (ans.upper() == "N" or ans.upper() == "NO"): 
                    quit = True
                    break

if __name__ == '__main__': 
    #username = useraccess.login()
    #create_playlist(username)
    #create_playlist("hi")
    #view_playlist(username)
    all_playlists = view_playlist("lh5844")
    rename_playlist("lh5844", all_playlists)