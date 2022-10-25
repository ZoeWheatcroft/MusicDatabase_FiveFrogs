import dbaccess
import useraccess

# search by name
def search_name(username): 
    quit = False
    while(not quit):
        word = input("What is the name of the song that you're searching for? ")
        lst = dbaccess.execute_query("SELECT s.title, s.length, u.play_history FROM song AS s LEFT OUTER JOIN userplayssong AS u ON ('s.songID' = 'u.songID') WHERE title LIKE '%" + word + "%' ORDER BY title ASC" )
        print(len(lst), "Songs found!")
        if len(lst) > 0: 
            for i in lst: 
                print(i)
        c = input("Would you like to search again? ")
        if c.upper()[0] == "N": 
            quit = True
    return None

if __name__ == '__main__': 
    username = useraccess.login()
    search_name(username)