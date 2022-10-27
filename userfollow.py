import dbaccess
import useraccess
import usersearch

def follow_user(username):
    quit = False
    while(not quit):
        word = input("What is the username of the user that you would like to follow? ")
        # TODO: SQL NEEDS TO CHECK IF THE USER IS ALREADY BEING FOLLOWED
        lst = dbaccess.execute_query("SELECT username from users WHERE username = '%s'"%(word))
        if len(lst) != 0: 
            lst = dbaccess.execute_query("SELECT username from userfollowsuser WHERE username = '%s' AND follows = '%s'" %(username, word))
            if len(lst) == 0:
                dbaccess.execute_start("INSERT INTO userfollowsuser (username, follows) \
                        VALUES ('"+ username +"', '"+ str(word) +"')")
                print("User %s has been followed." %(word))
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
        lst = dbaccess.execute_query("SELECT artist_name from artist WHERE artist_name = '%s'"%(word))
        if len(lst) != 0: 
            lst = dbaccess.execute_query("SELECT artist_name from userfollowsartist WHERE username = '%s' AND artist_name = '%s'" %(username, word))
            if len(lst) == 0:
                dbaccess.execute_start("INSERT INTO userfollowsartist (username, artist_name) \
                        VALUES ('"+ username +"', '"+ str(word) +"')")
                print("Artist %s has been followed." %(word))
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
                WHERE username = '"+ username +"' AND artist_name = '"+ str(word) +"'")
        else: 
            print("You do not follow this artist.")
        c = input("Would you like to unfollow another artist? ")
        if c.upper()[0] == 'N':
            quit = True

def unfollow_user(username):
    quit = False
    while(not quit):
        word = input("What is the username of the user that you would like to unfollow? ")
        lst = dbaccess.execute_query("SELECT username FROM userfollowsuser WHERE username = '%s' AND follows = '%s'" %(username, word))
        if len(lst) != 0:
            dbaccess.execute_start("DELETE FROM userfollowsuser \
                WHERE username = '"+ username +"' AND follows = '"+ str(word) +"'")
        else: 
            print("You do not follow this user.")
        c = input("Would you like to unfollow another user? ")
        if c.upper()[0] == 'N':
            quit = True

def follow_screen(username):
    print("What would you like to do?")
    print("1. Follow another user")
    print("2. Unfollow another user")
    print("3. Follow an artist")
    print("4. Unfollow an artist")
    num = input("Enter your selection here: [1, 2] ")
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
        else:
            num = input("Incorrect value. Please try again: [1, 2] ")

if __name__ == '__main__':
    username = useraccess.login()
    follow_screen(username)