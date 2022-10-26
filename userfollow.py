import dbaccess
import useraccess
import usersearch

def follow_user(username):
    quit = False
    lst = None
    while(not quit):
        word = input("What is the email of the user that you would like to follow? ")
        # TODO: SQL NEEDS TO CHECK IF THE USER IS ALREADY BEING FOLLOWED
        lst = dbaccess.execute_query("INSERT INTO userfollowsuser (username, follows) \
                VALUES ('"+ username +"', '"+ str(word) +"')")
        c = input("Would you like to follow another user? ")
        if c.upper()[0] == 'N':
            quit = True
    return lst

def unfollow_user(username):
    quit = False
    lst = None
    while(not quit):
        word = input("What is the email of the user that you would like to unfollow? ")
        lst = dbaccess.execute_query("DELETE FROM userfollowsuser \
                WHERE username = '"+ username +"' AND follows = '"+ str(word) +"'")
        c = input("Would you like to unfollow another user? ")
        if c.upper()[0] == 'N':
            quit = True
    return lst

def follow_screen(username):
    print("What would you like to do?")
    print("1. follow a user")
    print("2. unfollow a user")
    num = input("Enter your selection here: [1, 2] ")
    valid = False
    while not valid:
        if num == "1":
            valid = True
            follow_user(username)
        elif num == "2":
            valid = True
            unfollow_user(username)
        else:
            num = input("Incorrect value. Please try again: [1, 2] ")

if __name__ == '__main__':
    username = useraccess.login()
    follow_screen(username)