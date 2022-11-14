import dbaccess
import useraccess as u
import random as r
import datetime
import playlist as p
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



def user_profile(username):
    collection_num = get_collection_num(username)
    follower_num = get_follower_num(username)
    following_num = get_following_num(username)
    print("You have " + collection_num + " playlists")
    print("You have " + follower_num + " different followers")
    print("You follow " + following_num + " different users")
    