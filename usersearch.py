import dbaccess
import useraccess as u

# search by email
def search_email(): 
    quit = False
    lst = None
    while(not quit):
        word = input("What is the email of the user that you're searching for? ")
        lst = dbaccess.execute_query("SELECT u.username, u.email \
                FROM users AS u \
                WHERE u.email LIKE %s \
                ORDER BY u.username ASC", ("%"+word+"%", ))
        print(len(lst), "Users Found!")
        if len(lst) > 0: 
            for i in lst: 
                print("User Name: %16s | Email: %18s" % (i[0], i[1]))
        
        quit = u.keep_asking("Would you like to search again?")
    return lst


if __name__ == '__main__':
    username = u.login()
    #search_email(username)