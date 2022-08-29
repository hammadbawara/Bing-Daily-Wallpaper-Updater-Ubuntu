#!/usr/bin/python3

import WallpaperManager as wm
import os
from termcolor import colored

FILES_LIST_BEFORE_DOWNLOADING = os.listdir(wm.WALLPAPER_FOLDER_PATH)

# Checking if today wallpaper is already downloaded

if wm.is_today_wallpaper_downloaded():
    print(colored("TODAY WALLPAPER IS ALREADY DOWNLOADED.", "green"))
    exit(0)

NEW_WALLPAPERS_LIST = []
for i in range(0, 8):
    wallpaper = wm.download(i)
    if wallpaper != "":
        NEW_WALLPAPERS_LIST.append(wallpaper)
        if i == 0:
            wm.set_wallpaper(wallpaper)
            # The name of the wallpaper is like this 20220801.jpg.
            # The name of wallpaper also represent the date
            DATE = wallpaper.split(".")[0]
            wm.update_data_in_record_file(DATE, 2)
    else:
        print(colored("------ WALLPAPER NOT DOWNLOADED ---------"))
# If all wallpapers downloaded then delete older wallpapers
if len(NEW_WALLPAPERS_LIST) == 8:
    wm.delete_older_wallpapers(NEW_WALLPAPERS_LIST)
