#!/usr/bin/python3

import WallpaperManager as wm
import os
from termcolor import colored

FILES_LIST_BEFORE_DOWNLOADING = os.listdir(f"/home/{os.getlogin()}/.wallpapers")

NEW_WALLPAPERS_LIST = []
for i in range(0, 8):
    wallpaper = wm.download(i)
    if wallpaper != "":
        NEW_WALLPAPERS_LIST.append(wallpaper)
    else:
        print(colored("------ WALLPAPER NOT DOWNLOADED ---------"))
# If all wallpapers downloaded then delete older wallpapers
if len(NEW_WALLPAPERS_LIST)==8:
    wm.delete_older_wallpapers(NEW_WALLPAPERS_LIST)
# Setting wallpaper
if len(NEW_WALLPAPERS_LIST) > 0 :
    if NEW_WALLPAPERS_LIST[0] not in FILES_LIST_BEFORE_DOWNLOADING:
        wm.set_wallpaper(NEW_WALLPAPERS_LIST[0])
