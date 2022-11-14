import dbaccess
import useraccess as u
import random as r
import datetime
import playlist as p
import foryou
from userfollow import print_list


def get_collection_num(username):
    
    #get num playlists that user has 
    get_playlist = "SELECT COUNT playlist_id from usercreatesplaylist where username = '%s'" % (username)
    num_playlists = dbaccess.execute_query(get_playlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    return num_playlists

def get_follower_num(username):
    
    #get num followers that user has 
    get_followers = "SELECT COUNT follows from userfollowsuser where username = '%s'" % (username)
    num_followers = dbaccess.execute_query(get_followers)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    return num_followers

def get_following_num(username):
    
    #get num users that user is following
    get_following = "SELECT COUNT username from userfollowsuser where follows = '%s'" % (username)
    num_following = dbaccess.execute_query(get_following)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    return num_following

def get_top_10_artists(username):

    #get top 10 artists for user by plays
    top_artists = "SELECT a.artist_name, count(*) listen_total \
                    FROM userplayssong AS s \
                    INNER JOIN artistcreatessong AS a ON (s.song_id = a.song_id)\
                    WHERE s.username = '%s'\
                    GROUP BY s.song_id, a.artist_name \
                    ORDER BY listen_total DESC \
                    LIMIT 10" % (username)
    artist_list = dbaccess.execute_query(top_artists)
    print(artist_list)

def user_stats(username):
    collection_num = get_collection_num(username)
    follower_num = get_follower_num(username)
    following_num = get_following_num(username)
    print("You have " + collection_num + " playlists")
    print("You have " + follower_num + " different followers")
    print("You follow " + following_num + " different users")

def print_options():
    print("  1. Get user stats")
    print("  2. See your top 10 artists")
    print("  3. See recommended songs")
    print("  4. Exit")

def user_profile_screen(username):
    print_options()
    num = input("[1, 2, 3, 4]: ")
    valid = False
    while not valid:
        #play song
        if num == "1": 
            valid = True
            user_stats(username)
        #sort by 
        elif num == "2":
            valid = True 
            get_top_10_artists(username)
        elif num == "3":
            valid = True 
            foryou.fyp(username)
        elif num == "4":
            #quit = True
            break
        elif num == "h" or num == "H":
            print_options()
        #got bad input
        else: 
            num = input("Incorrect value. Please try again: [1, 2, 3, 4] ")
    return

if __name__ == '__main__': 
    user_profile_screen("hannakoh")