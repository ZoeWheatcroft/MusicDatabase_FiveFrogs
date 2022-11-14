import dbaccess as d
from securepass import encrypt
import datetime


def keep_asking(question):
    while(True):
        ans = input("%s [Y/N] " % (question))
        if (ans.upper() == "Y" or ans.upper() == "YES"): 
            break
        if (ans.upper() == "N" or ans.upper() == "NO"): 
            return True
        print("Invalid input: Type one of the following ['Y'/'Yes'/'N'/'No']")


def login(): 
    # DO NOT CHANGE THIS. WE WON'T BE ABLE TO LOG IN
    salt = b'$2b$12$XbsaQmKwYQdGhscNuKqGaO'
    username = input("Enter your username: ")
    lst = d.execute_query("SELECT username, password from users WHERE username = %s", (username, ))

    if len(lst) != 0:
        password = input("Enter your password: ")
        password = encrypt(password, salt)
        while password != lst[0][1].encode(): 
            password = input("Password incorrect. Please try again: ")
        print("Password successful! Logged in as", username)
        d.execute_start("UPDATE users SET last_access = %s WHERE username = %s" (datetime.datetime.now(), username))
        return username
    elif len(lst) == 0: 
        while(True):
            cond = input("Account not found.\nWould you like to create an acccount? [Y/N] ")
            if cond.capitalize()[0] == "Y" or cond.upper() == "YES": 
                # check for proper email formatting for later?
                email = input("Enter your email address: ")
                first = input("Enter your first name: ")
                last = input("Enter your last name: ")
                password = input("Enter a password: ")
                password = encrypt(password, salt).decode('utf-8')
                creation_time = datetime.datetime.now()
                sqlstring = "INSERT into users (username, creation_date, first_name, last_name, email, password, last_access) VALUES(%s, %s, %s, %s, %s, %s, %s);"
                d.execute_start(sqlstring, (username, creation_time, first, last, email, password, creation_time))
                return username
            if cond.capitalize()[0] == "N" or cond.upper() == "NO":
                break
            print("Invalid input: Type one of the following ['Y'/'Yes'/'N'/'No']")
    return None

if __name__ == '__main__': 
    print(login())

