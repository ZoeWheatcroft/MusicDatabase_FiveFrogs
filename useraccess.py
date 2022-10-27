import dbaccess
import datetime

def login(): 
    username = input("Enter your username: ")
    lst = dbaccess.execute_query("SELECT username, password from users WHERE username = '%s'" % (username))
    # MAKE SURE TO DELETE this later
    print(lst)
    if len(lst) != 0:
        password = input("Enter your password: ")
        while password != lst[0][1]: 
            password = input("Password incorrect. Please try again: ")
        print("Password successful! Logged in as", username)
        dbaccess.execute_start("UPDATE users SET last_access = '%s' WHERE username = '%s'" % (datetime.datetime.now(), username))
        return username
    elif len(lst) == 0: 
        cond = input("Account not found. Would you like to create an acccount? ")
        if cond.capitalize()[0] == "Y": 
            # check for proper email formatting for later?
            email = input("Enter your email address: ")
            first = input("Enter your first name: ")
            last = input("Enter your last name: ")
            password = input("Enter a password: ")
            creation_time = datetime.datetime.now()
            sqlstring = "INSERT into users (username, creation_date, first_name, last_name, email, password, last_access) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (username, creation_time, first, last, email, password, creation_time)
            dbaccess.execute_start(sqlstring)
            return username
    return None

if __name__ == '__main__': 
    print(login())

