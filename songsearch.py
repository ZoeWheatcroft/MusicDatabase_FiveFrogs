import dbaccess
import useraccess

# search by name
def search_name(username): 
    quit = False
    while(not quit):
        word = input("What is the name of the song that you're searching for? ")
        lst = dbaccess.execute_query("SELECT title, length, listen_count from song WHERE title LIKE '%" + word + "%' ORDER BY title ASC" )
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print("Song Title: %18s | Length (sec): %2d | Number of plays: %3d" % (i[0], i[1], i[2]))
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return None

if __name__ == '__main__': 
    #username = useraccess.login()
    search_name("hi")