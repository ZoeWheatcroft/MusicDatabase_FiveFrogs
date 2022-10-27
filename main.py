import dbaccess
import useraccess as u
import songsearch as s
import collection as p
import userfollow as f

def main(): 
    user = u.login()
    quit = False
    while not quit: 
        valid = False
        while not valid:
            print("What would you like to do?")
            print("1. Search for a song")
            print("2. View your playlists")
            print("3. Follow/unfollow a friend")
            num = input("[1, 2, 3]: ")
            if num == "1": 
                valid = True
                s.search_screen(user)
            elif num == "2": 
                valid = True
                p.view_playlist(user)
            elif num == "3": 
                valid = True
                f.follow_screen(user)
            else:
                num = input("Incorrect value. Please try again: [1, 2, 3] ")
        yn = input("Do you want to do something else? [y/n] ")
        if yn.lower()[0] == "n": 
            quit = True

if __name__ == '__main__': 
    main()