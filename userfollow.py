import imp
import dbaccess
import useraccess
import usersearch

# follow a user 
def follow_user(username):
    quit = False
    lst = None
    while(not quit):
        word = input("What is the email of the user that you would like to follow? ")
        # TODO: SQL NEEDS TO CHECK IF THE USER IS ALREADY BEING FOLLOWED
        lst = dbaccess.execute_query("UPDATE userfollowsuser \
            SET follows = CONCAT('"+username+"', ', ', follows) \
            WHERE username = '"+username+"'")
        c = input("Would you like to follow another user? ")
        if c.upper()[0] == 'N':
            quit = True
    return lst 

def unfollow_user(username):
    return 0

if __name__ == '__main__':
    username = useraccess.login()
    follow_user(username)