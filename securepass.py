import bcrypt as b
import dbaccess as d
import datetime

def encrypt(password, salt): 
    passw = bytes(password, 'utf-8')
    #salt =  bytes('frog123', 'uft-8')
    hashed = b.hashpw(passw, salt)
    return hashed

def updatepass(): 
    lst = d.execute_query("SELECT username, password FROM users")
    for l in lst: 
        print("Encrypting %s's password." )
        password = encrypt(l[1], salt).decode('utf-8')
        d.execute_start("UPDATE users SET password = '%s' WHERE username = %s", (password, l[0]))

if __name__ == '__main__': 
    salt = b'$2b$12$XbsaQmKwYQdGhscNuKqGaO'
    updatepass()