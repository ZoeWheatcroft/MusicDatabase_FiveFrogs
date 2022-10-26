import imp
import dbaccess
import useraccess
import usersearch

# follow a user 
def follow_user(username):
    return 0


if __name__ == '__main__':
    username = useraccess.login()
    follow_user(username)