#!/usr/bin/python3

import WallpaperManager as wm
import os

FILES_LIST_BEFORE_DOWNLOADING = os.listdir()

NEW_WALLPAPERS_LIST = []
for i in range(0, 8):
    wallpaper = wm.download(i)
    NEW_WALLPAPERS_LIST.append(wallpaper)
# If all wallpapers downloaded then delete older wallpapers
if len(NEW_WALLPAPERS_LIST)==8:
    wm.delete_older_wallpapers(NEW_WALLPAPERS_LIST)
# Setting wallpaper
if NEW_WALLPAPERS_LIST[0] not in FILES_LIST_BEFORE_DOWNLOADING:
    wm.set_wallpaper(NEW_WALLPAPERS_LIST[0])
