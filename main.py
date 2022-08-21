import os
import sys
import WallpaperManager as wm

# checking operating system if it is linux then use linux then run the script 
if os.name != 'posix':
    print(colored('[-] This program is only made for linux', 'red'))
    exit()

# checking if Desktop enviroment is gnome then run the script
if os.getenv('DESKTOP_SESSION') != 'ubuntu':
    print(colored('[-] This program is not tested for this distro.', 'red'))
    exit()

args = sys.argv

if len(args) == 1:
    file_name = wm.download()
    wm.set_wallpaper(file_name)
    exit()

if args[1] == '-h' or args[1] == '--help':
    print("-d, download  -  Downloads the wallpaper the today wallpaper")
    print("-ds, download-set, update-wallpaper, -uw -  Downloads and sets the wallpaper the today wallpaper")
    print("-sr, set-random -  Sets random wallpaper on Desktop")
    exit()

elif args[1] == 'download' or args[1] == '-d':
    wm.download()

elif args[1] ==  '-ds' or args[1] == 'download-set' or args[1] == 'update-wallpaper' or args[1] == '-uw':
    file_name = wm.download()
    wm.set_wallpaper(file_name)

elif args[1] == 'set-random' or args[1] == '-sr':
    wm.set_random()

else:
    print("option not found")