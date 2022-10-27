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
            ans = input("Would you like to create another playlist? [Y/N] ")
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
    print("%11s ~*~ Your Playlists ~*~" % (" "))
    print("-----------------------------------------------")
    print("%16s | %15s | %8s" % ("Playlist Name", "Number of Songs", "Duration"))
    print("-----------------------------------------------")
    #check if user has any playlists or not 
    show_playlist = "SELECT playlist_id from usercreatesplaylist where username = '%s'" % (username)
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
            duration = convert_mins(playlist[2])
            print("%16s | %9s songs | %8s" % (playlist[0], playlist[1], duration))
        
    your_playlist_screen(username)

def rename_playlist(username):
    show_playlist = "SELECT playlist_id from usercreatesplaylist where username = '%s'" % (username)
    user_playlists = dbaccess.execute_query(show_playlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if not user_playlists: 
        print("Error: No playlists available to rename")
    else: 
        quit = False
        while(not quit):
            rename = input("Which playlist do you want to rename? ")
            #check if that playlist name exists 
            select_check_exists = "SELECT playlist_name from playlist WHERE playlist_name = '%s'" % (rename)
            check_exists = dbaccess.execute_query(select_check_exists)
            if not check_exists:
                print("Error: '%s' does not exist" % (rename))
            else: 
                name = input("What do you want to name it to? ")
                #update playlist_name only if playlist_id is the right one
                select_rename_id = "SELECT p.playlist_id \
                            FROM playlist AS p \
                            LEFT JOIN usercreatesplaylist AS u on (p.playlist_id = u.playlist_id) \
                            WHERE u.username = '%s' AND p.playlist_name = '%s'" % (username, rename)
                rename_id = dbaccess.execute_query(select_rename_id)
                dbaccess.execute_start("UPDATE playlist SET playlist_name = '%s' \
                                        WHERE playlist_id = '%s'" % (name, rename_id[0][0]))

                print("'%s' renamed to '%s'" % (rename, name))

            #keep asking if want to rename another playlist until valid answer given 
            while(True):
                ans = input("Would you like to rename another playlist? [Y/N] ")
                if (ans.upper() == "Y" or ans.upper() == "YES"): 
                    break
                if (ans.upper() == "N" or ans.upper() == "NO"): 
                    quit = True
                    break
    
def delete_playlist(username):
    show_playlist = "SELECT playlist_id from usercreatesplaylist where username = '%s'" % (username)
    user_playlists = dbaccess.execute_query(show_playlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if not user_playlists: 
        print("Error: No playlists available to delete")
    else: 
        quit = False
        while(not quit):
            delete_name = input("Which playlist do you want to delete? ")
            #check if that playlist name exists 
            select_check_exists = "SELECT playlist_name from playlist WHERE playlist_name = '%s'" % (delete_name)
            check_exists = dbaccess.execute_query(select_check_exists)
            if not check_exists:
                print("Error: '%s' does not exist" % (delete_name))
            else: 
                #delete playlist only if playlist_id is the right one
                select_rename_id = "SELECT p.playlist_id \
                            FROM playlist AS p \
                            LEFT JOIN usercreatesplaylist AS u on (p.playlist_id = u.playlist_id) \
                            WHERE u.username = '%s' AND p.playlist_name = '%s'" % (username, delete_name)
                rename_id = dbaccess.execute_query(select_rename_id)

                dbaccess.execute_start("DELETE FROM usercreatesplaylist WHERE playlist_id = '%s'" % (rename_id[0][0]))
                dbaccess.execute_start("DELETE FROM playlistcontainssong WHERE playlist_id = '%s'" % (rename_id[0][0]))
                dbaccess.execute_start("DELETE FROM playlist WHERE playlist_id = '%s'" % (rename_id[0][0]))

                print("'%s' has been deleted" % (delete_name))

            #keep asking if want to delete another playlist until valid answer given 
            while(True):
                ans = input("Would you like to delete another playlist? [Y/N] ")
                if (ans.upper() == "Y" or ans.upper() == "YES"): 
                    break
                if (ans.upper() == "N" or ans.upper() == "NO"): 
                    quit = True
                    break

def your_playlist_screen(username):
    valid = False
    while not valid:
        print("Your Playlist Options:")
        print("1. Select a playlist")
        print("2. Rename a playlist")
        print("3. Delete a playlist")
        print("4. Exit")
        num = input("[1, 2, 3, 4]: ")
        if num == "1":
            valid = True
            #view_playlist(username)
            print("work in progress but should lead to list of songs under a playlist")
        elif num == "2":
            valid = True
            rename_playlist(username)
        elif num == "3":
            valid = True
            delete_playlist(username)
        elif num == "4":
            break
        else:
            num = input("Incorrect value. Please try again: [1, 2, 3, 4] ")

if __name__ == '__main__': 
    #username = useraccess.login()
    #create_playlist("lh5844")
    #create_playlist("hi")
    #view_playlist(username)
    all_playlists = view_playlist("hannakoh")
    
    #rename_playlist("lh5844", all_playlists)
    #delete_playlist("lh5844", all_playlists)