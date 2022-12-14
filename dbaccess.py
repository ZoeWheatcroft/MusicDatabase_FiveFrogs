import psycopg2
from sshtunnel import SSHTunnelForwarder
import json

#This executes a statement and then closes the connection. 
def execute_start(str, values):
    conn = None
    try:
        json_object = None
        with open('login.json', 'r') as openfile:
            json_object = json.load(openfile)

        username = json_object["user"]
        password = json_object["password"]
        dbName = json_object["database"]
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('localhost', 5432)) as server:
            server.start()
            #print("SSH tunnel established")
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(str, values)
            #print("Database connection established")
            conn.commit()
    except:
        print("Connection failed")
    finally: 
        if conn != None: 
            conn.close()


# This returns what is stored in the cursor
def execute_query(str, values):
    conn = None
    try:
        json_object = None
        with open('login.json', 'r') as openfile:
            json_object = json.load(openfile)

        username = json_object["user"]
        password = json_object["password"]
        dbName = json_object["database"]
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('localhost', 5432)) as server:
            server.start()
            #print("SSH tunnel established")
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(str, values)
            lst = []
            for s in curs: 
                lst.append(s)
            #print("Database connection established")
            conn.close()
            return lst
    except:
        print("Connection failed")
        return []
    finally: 
        if conn != None: 
            conn.close()

if __name__ == '__main__': 
    #execute_start("SELECT * FROM user")
    print(execute_query("SELECT * FROM "))