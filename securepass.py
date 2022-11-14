import bcrypt as b
import dbaccess as d
import datetime
def encrypt(password, salt): 
    passw = bytes(password, 'utf-8')
    #salt =  bytes('frog123', 'uft-8')
    hashed = b.hashpw(passw, salt)
    return hashed


def logintest(): 
    salt = b'$2b$12$XbsaQmKwYQdGhscNuKqGaO'
    username = input("Enter your username: ")
    lst = d.execute_query("SELECT username, password from users WHERE username = '%s'" % (username))

    if len(lst) != 0:
        password = input("Enter your password: ")
        # WHAT NEEDS TO BE CHANGED IS HERE!!
        password = encrypt(password, salt)
        while password != lst[0][1].encode(): 
            # these two lines :)
            password = input("Password incorrect. Please try again: ")
        print("Password successful! Logged in as", username)
        d.execute_start("UPDATE users SET last_access = '%s' WHERE username = '%s'" % (datetime.datetime.now(), username))
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
                # ADD THIS ALSO
                password = encrypt(password, salt).decode('utf-8')
                # ^^^^^^^^^^^^^^^^^^^^
                creation_time = datetime.datetime.now()
                sqlstring = "INSERT into users (username, creation_date, first_name, last_name, email, password, last_access) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (username, creation_time, first, last, email, password, creation_time)
                d.execute_start(sqlstring)
                return username
            if cond.capitalize()[0] == "N" or cond.upper() == "NO":
                break
            print("Invalid input: Type one of the following ['Y'/'Yes'/'N'/'No']")
    return None

def updatepass(): 
    lst = d.execute_query("SELECT username, password FROM users")
    for l in lst: 
        print("Encrypting %s's password." )
        password = encrypt(l[1], salt).decode('utf-8')
        d.execute_start("UPDATE users SET password = '%s' WHERE username = '%s'" % (password, l[0]))

if __name__ == '__main__': 
    salt = b'$2b$12$XbsaQmKwYQdGhscNuKqGaO'
    updatepass()