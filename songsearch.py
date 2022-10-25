import dbaccess
import useraccess

# need to figure out how to also get user's number of times listened
def search_name(username): 
    word = input("What is the name of the song that you're searching for? ")
    lst = dbaccess.execute_query("SELECT title, length FROM song WHERE title LIKE '%" + word + "%' ORDER BY title ASC" )
    if len(lst) > 0: 
        for i in lst: 
            print(i)

if __name__ == '__main__': 
    username = useraccess.login()
    search_name(username)