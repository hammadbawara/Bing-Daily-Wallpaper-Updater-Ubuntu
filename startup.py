#!/usr/bin/python3

import WallpaperManager as wm
import os
from termcolor import colored
import time

FILES_LIST_BEFORE_DOWNLOADING = os.listdir(wm.WALLPAPER_FOLDER_PATH)

# Checking if today wallpaper is already downloaded

if wm.is_today_wallpaper_downloaded():
    print(colored("TODAY WALLPAPER IS ALREADY DOWNLOADED.", "green"))
    exit(0)

wait_time = 2
while True:
    wallpaper = wm.download(0)
    if wallpaper == "":
        time.sleep(wait_time)
        wait_time = wait_time*2
        if wait_time > 128:
            break
    else:
        wm.set_wallpaper(wallpaper)
        # The name of the wallpaper is like this 20220801.jpg.
        # The name of wallpaper also represent the date
        DATE = wallpaper.split(".")[0]
        wm.update_data_in_record_file(DATE, 2)
        break



NEW_WALLPAPERS_LIST = []
for i in range(1, 8):
    wallpaper = wm.download(i)
    if wallpaper != "":
        NEW_WALLPAPERS_LIST.append(wallpaper)
    else:
        print(colored("------ WALLPAPER NOT DOWNLOADED ---------"))
# If all wallpapers downloaded then delete older wallpapers
if len(NEW_WALLPAPERS_LIST) == 8:
    wm.delete_older_wallpapers(NEW_WALLPAPERS_LIST)
