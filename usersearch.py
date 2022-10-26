import dbaccess
import useraccess

# search by name
def search_name(username): 
    quit = False
    lst = None
    while(not quit):
        word = input("What is the name of the user that you're searching for? ")
        lst = dbaccess.execute_query("SELECT u.username \
                FROM user AS u \
                ORDER BY u.username ASC")
        print(len(lst), "Users Found!")
        if len(lst) > 0: 
            for i in lst: 
                print("User Name: %16u" % (i[0]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return lst


if __name__ == '__main__':
    username = useraccess.login()
    search_name(username)