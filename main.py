import dbaccess
import useraccess as u
import songsearch as s
import collection as p
import userfollow as f
import playsong as ps
import userprofile as frog_rider
            

def main():
    user = u.login()
    if user == None: 
        print("Exiting...")
        return 0
    quit = False
    while not quit:
        valid = False
        while not valid:
            print("What would you like to do?")
            print("  1. Search for a song")
            print("  2. Play a song")
            print("  3. View playlist options")
            print("  4. Follow/unfollow a friend")
            print("  5. View your profile")
            print("  6. Exit")
            num = input("[1, 2, 3, 4, 5, 6]: ")
            if num == "1":
                valid = True
                s.search_screen()
            elif num == "2":
                valid = True
                ps.play_song(user)
            elif num == "3":
                valid = True
                p.playlist_options(user)
            elif num == "4":
                valid = True
                f.follow_screen(user)
            elif num == "5":
                valid = True
                frog_rider.user_profile_screen(user)
            elif num == "6":
                return 0
            else:
                num = input("Incorrect value. Please try again: [1, 2, 3, 4, 5, 6] ")

        quit = u.keep_asking("Do you want to do something else?")



if __name__ == '__main__':
    main()
