import dbaccess
import useraccess
import random as r

def create_playlist(username):
    quit = False
    while(not quit):
        name = input("What do you want to name your playlist? ")
        #check if it already exists and then regenerate 
        randomID = r.randint(1, 99999) #fix this for later so that it isn't randomly 
        playlistID = int('%i%i' % (30,randomID))
        print("playlistID", playlistID)
        #dbaccess.execute_start("In" )
        print("Playlist called '" + name + "' has been made")
    
        ans = input("Would you like to create another playlist? (Y/N)")
        if ans.upper()[0] == "N": 
            quit = True
if __name__ == '__main__': 
    #username = useraccess.login()
    create_playlist("hi")