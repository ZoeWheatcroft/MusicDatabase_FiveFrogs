import dbaccess
import useraccess
import usersearch

def follow_user(username):
    quit = False
    while(not quit):
        word = input("What is the username of the user that you would like to follow? ")
        # TODO: SQL NEEDS TO CHECK IF THE USER IS ALREADY BEING FOLLOWED
        lst = dbaccess.execute_query("SELECT username from users WHERE username = '%s'" % (word))
        if len(lst) != 0: 
            lst = dbaccess.execute_query("SELECT username from userfollowsuser WHERE username = '%s' AND follows = '%s'" % (username, word))
            if len(lst) == 0:
                dbaccess.execute_start("INSERT INTO userfollowsuser (username, follows) \
                        VALUES ('%s', '%s')" % (username, word))
                print("User %s has been followed." % (word))
            else: 
                print("User %s is already followed!" % (word))
        else: 
            print("User %s doesn't exist!" % (word))
        c = input("Would you like to follow another user? ")
        if c.upper()[0] == 'N':
            quit = True


def follow_artist(username):
    quit = False
    while(not quit):
        word = input("What is the name of the artist that you would like to follow? ")
        lst = dbaccess.execute_query("SELECT artist_name from artist WHERE artist_name = '%s'" % (word))
        if len(lst) != 0: 
            lst = dbaccess.execute_query("SELECT artist_name from userfollowsartist WHERE username = '%s' AND artist_name = '%s'" % (username, word))
            if len(lst) == 0:
                dbaccess.execute_start("INSERT INTO userfollowsartist (username, artist_name) \
                        VALUES ('%s', '%s')" % (username, word))
                print("Artist %s has been followed." % (word))
            else: 
                print("Artist %s is already followed!" % (word))
        else: 
            print("Artist %s doesn't exist!" % (word))
        c = input("Would you like to follow another artist? ")
        if c.upper()[0] == 'N':
            quit = True

def unfollow_artist(username):
    quit = False
    while(not quit):
        word = input("What is the name of the artist that you would like to unfollow? ")
        lst = dbaccess.execute_query("SELECT artist_name FROM userfollowsartist WHERE username = '%s' AND artist_name = '%s'" %(username, word))
        if len(lst) != 0:
            dbaccess.execute_start("DELETE FROM userfollowsartist \
                WHERE username = '%s' AND artist_name = '%s'" % (username, word) )
        else: 
            print("You do not follow this artist.")
        c = input("Would you like to unfollow another artist? ")
        if c.upper()[0] == 'N':
            quit = True

def unfollow_user(username):
    quit = False
    while(not quit):
        word = input("What is the username of the user that you would like to unfollow? ")
        lst = dbaccess.execute_query("SELECT username FROM userfollowsuser WHERE username = '%s' AND follows = '%s'" % (username, word))
        if len(lst) != 0:
            dbaccess.execute_start("DELETE FROM userfollowsuser \
                WHERE username = '%s' AND follows = '%s'" % (username, word))
        else: 
            print("You do not follow this user.")
        c = input("Would you like to unfollow another user? ")
        if c.upper()[0] == 'N':
            quit = True

def follow_screen(username):
    view_user_followlist(username)
    view_artist_followlist(username)
    dash_len = 36
    dash_str = "-" * dash_len
    print(dash_str)

    print("What would you like to do?")
    print("  1. Follow another user")
    print("  2. Unfollow another user")
    print("  3. Follow an artist")
    print("  4. Unfollow an artist")
    print("  5. Exit")
    num = input("Enter your selection here: [1, 2, 3, 4, 5] ")
    valid = False
    while not valid:
        if num == "1":
            valid = True
            follow_user(username)
        elif num == "2":
            valid = True
            unfollow_user(username)
        elif num == "3":
            valid = True
            follow_artist(username)
        elif num == "4":
            valid = True
            unfollow_artist(username)
        elif num == "5":
            break
        else:
            num = input("Incorrect value. Please try again: [1, 2, 3, 4, 5] ")

def view_user_followlist(username):
    #maybe make a function later to pretty print
    dash_len = 36
    dash_str = "-" * dash_len
    print(dash_str)
    print("%s" % ("~*~ Your User Following ~*~".center(dash_len)))
    print(dash_str)

    show_followlist = "SELECT follows from userfollowsuser where username = '%s' \
                        ORDER BY follows ASC" % (username)
    user_followlist = dbaccess.execute_query(show_followlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if not user_followlist: 
        print("You are not following any users")
    else: 
        for user in user_followlist:
            print("%s" % (user[0].center(dash_len)))

def view_artist_followlist(username):
    dash_len = 36
    dash_str = "-" * dash_len
    print(dash_str)
    print("%s" % ("~*~ Your Artist Following ~*~".center(dash_len)))
    print(dash_str)

    show_followlist = "SELECT artist_name from userfollowsartist where username = '%s' \
                        ORDER BY artist_name ASC" % (username)
    user_followlist = dbaccess.execute_query(show_followlist)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    if not user_followlist: 
        print("You are not following any artists")
    else: 
        for user in user_followlist:
            print("%s" % (user[0].center(dash_len)))

if __name__ == '__main__':
    #username = useraccess.login()
    #follow_screen(username)
    view_artist_followlist("lh5844")