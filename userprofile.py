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
    return artist_list

def user_profile(username):
    collection_num = get_collection_num(username)
    follower_num = get_follower_num(username)
    following_num = get_following_num(username)
    artist_list = get_top_10_artists(username)
    print("You have " + collection_num + " playlists")
    print("You have " + follower_num + " different followers")
    print("You follow " + following_num + " different users")
    
    


if __name__ == '__main__': 
    get_top_10_artists("hannakoh")