import os
import sys
import WallpaperManager as wm
from termcolor import colored

# checking operating system if it is linux then use linux then run the script 
if os.name != 'posix':
    print(colored('[-] This program is only made for linux', 'red'))
    exit()

# checking if Desktop environment is gnome then run the script
if os.getenv('DESKTOP_SESSION') != 'ubuntu':
    print(colored('[-] This program is not tested for this distro.', 'red'))
    exit()

args = sys.argv

if __name__ == '__main__':
    if len(args) == 1:
        file_name = wm.download()
        wm.set_wallpaper(file_name)
        exit()
else:
    exit()

if args[1] == '-h' or args[1] == '--help':
    print("-d, download  -  Downloads the wallpaper the today wallpaper")
    print("-ds, download-set, update-wallpaper, -uw -  Downloads and sets the wallpaper the today wallpaper")
    print("-sr, set-random -  Sets random wallpaper on Desktop")
    print("-next, next -  Sets next wallpaper on Desktop")
    print("-prev, previous -  Sets previous wallpaper on Desktop")
    print("-l, latest -  Sets latest wallpaper on Desktop")
    print("-sw, set-wallpaper - Set Wallpaper [FILE]")
    exit()

elif args[1] == 'download' or args[1] == '-d':
    wm.download()

elif args[1] == '-ds' or args[1] == 'download-set' or args[1] == 'update-wallpaper' or args[1] == '-uw':
    NEW_WALLPAPERS_LIST = []
    for i in range(0, 8):
        wallpaper = wm.download(i)
        NEW_WALLPAPERS_LIST.append(wallpaper)
    # If all wallpapers downloaded then delete older wallpapers
    if len(NEW_WALLPAPERS_LIST)==8:
        wm.delete_older_wallpapers(NEW_WALLPAPERS_LIST)
    # Setting wallpaper
    wm.set_wallpaper(NEW_WALLPAPERS_LIST[0])

elif args[1] == 'set-random' or args[1] == '-sr':
    wm.set_random()

elif args[1] == 'next' or args[1] == '-next':
    wm.set_next_wallpaper()

elif args[1] == 'prev' or args[1] == "previous" or args[1] == '-prev':
    wm.set_next_wallpaper(True)

elif args[1] == 'latest' or args[1] == '-l':
    wm.set_latest_wallpaper()

elif args[1] == 'set-wallpaper' or args[1] == '-sw':
    if len(args) == 2:
        wallpaper = args[2]
        wm.set_wallpaper(wallpaper)
    else:
        print("set-wallpaper accepts only one file name more than one file name given.")

else:
    print("option not found")
