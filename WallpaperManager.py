import datetime
import json
import os
import random

import requests
from termcolor import colored
from tqdm import tqdm

# Global Variables
WALLPAPER_FOLDER_PATH = f"/home/{os.getlogin()}/.wallpapers"
WALLPAPER_RECORD_FILE = f'{WALLPAPER_FOLDER_PATH}/current_wallpaper.txt'

CURRENT_WALLPAPER = ""

if not os.path.isdir(WALLPAPER_FOLDER_PATH):
    os.mkdir(WALLPAPER_FOLDER_PATH)
if not os.path.isfile(WALLPAPER_RECORD_FILE):
    with open(WALLPAPER_RECORD_FILE, "w") as f:
        f.write("wallpaper.png\n date")
with open(WALLPAPER_RECORD_FILE) as f:
    CURRENT_WALLPAPER = f.readline().strip()


def download(index=0):
    """
    Parameters
    ----------
    index : int, optional index is the day of image you want to download. e.g 0 mean day 1 and up to 7.
    """

    region = "en-US"
    api_url = f"https://bing.biturl.top/?resolution=1920&format=json&index={index}&mkt={region}"

    print("-------Connecting to server-------")
    while True:
        try:
            response = requests.get(api_url)
            break
        except Exception:
            print(colored("\n------ FAILED TO CONNECT SERVER  ------.", "red"))
            return ""
    print(colored("\n------ SERVER CONNECTION SUCESSFUL ------)", "green"))

    # Making list from json response
    response = json.loads(response.text)

    print(colored(f"\n------ DOWNLOADING WALLPAPER ------{index + 1}\n", "blue"))
    wallpaper_file_name = response['start_date'] + ".jpg"

    # check if wallpaper already exists
    global WALLPAPER_FOLDER_PATH
    if os.path.isfile(f'{WALLPAPER_FOLDER_PATH}/{wallpaper_file_name}'):
        print(colored("\n------ WALLPAPER ALREADY EXISTS ------", "red"))
        return wallpaper_file_name

    # Downloading the wallpaper
    try:
        with requests.get(response["url"], stream=True) as r:
            r.raise_for_status()
            with open(f'{WALLPAPER_FOLDER_PATH}/{wallpaper_file_name}', "wb") as image_file:
                for chunk in tqdm(r.iter_content(chunk_size=1024)):
                    image_file.write(chunk)
                    image_file.flush()
    except:
        return ""

    print(colored("\n------ WALLPAPER DOWNLOADED ------", "green"))

    return wallpaper_file_name


def set_wallpaper(wallpaper_file_name: str):
    wallpaper_image_path = f'{WALLPAPER_FOLDER_PATH}/{wallpaper_file_name}'

    # For Dark Theme
    os.system(f"gsettings set org.gnome.desktop.background picture-uri-dark 'file://{wallpaper_image_path}'")

    # For Light Theme
    os.system(f"gsettings set org.gnome.desktop.background picture-uri 'file://{wallpaper_image_path}'")

    print(colored("WALLPAPER SET : " + wallpaper_file_name, "green"))
    global CURRENT_WALLPAPER
    CURRENT_WALLPAPER = wallpaper_file_name

    update_data_in_record_file(wallpaper_file_name, 1)


def set_random():
    wallpapers = os.listdir(WALLPAPER_FOLDER_PATH)
    wallpaper = wallpapers[random.randint(0, len(wallpapers) - 1)]
    set_wallpaper(wallpaper)


def set_next_wallpaper(previous=False):
    if not os.path.isfile(WALLPAPER_RECORD_FILE):
        print(colored("RECORD FILE DOES NOT EXIST", "red"))
        set_latest_wallpaper()
        return

    with open(WALLPAPER_RECORD_FILE) as f:
        current_wallpaper = f.readline().strip()
        print(current_wallpaper)

    if current_wallpaper == "":
        print(colored("CURRENT WALLPAPER DOES NOT EXIST", "red"))
        set_latest_wallpaper()
        return

    wallpapers_list = os.listdir(WALLPAPER_FOLDER_PATH)

    # removing other files
    for index, wallpaper in enumerate(wallpapers_list):
        if not wallpaper.endswith(".jpg") or wallpaper.endswith(".JPG"):
            wallpapers_list.pop(index)

    wallpapers_list.sort(reverse=True)

    is_current_wallpaper_found = False
    for index, wallpaper in enumerate(wallpapers_list):
        if wallpaper == current_wallpaper:
            is_current_wallpaper_found = True
            if previous == True:
                if index + 1 == len(wallpapers_list):
                    print(colored("THERE IS NO PREVIOUS WALLPAPER", "blue"))
                else:
                    set_wallpaper(wallpapers_list[index + 1])
                    break
            else:
                if index == 0:
                    print(colored("THERE IS NO NEXT WALLPAPER", "blue"))
                else:
                    set_wallpaper(wallpapers_list[index - 1])
                    break

    if not is_current_wallpaper_found:
        print(colored("CURRENT WALLPAPER DOES NOT EXIST", "red"))
        if len(wallpapers_list) > 0:
            set_latest_wallpaper()


def set_latest_wallpaper():
    wallpapers_list = os.listdir(WALLPAPER_FOLDER_PATH)

    # removing other files
    for index, wallpaper in enumerate(wallpapers_list):
        if not wallpaper.endswith(".jpg") or wallpaper.endswith(".JPG"):
            wallpapers_list.pop(index)

    wallpapers_list.sort(reverse=True)

    if len(wallpapers_list) > 0:
        set_wallpaper(wallpapers_list[0])
    else:
        print(colored("THERE IS NO DOWNLOADED WALLPAPER", "blue"))


def download_complete_week_wallpaper():
    wallpaper = ""
    for i in range(0, 7, -1):
        wallpaper = download(i)
    set_wallpaper(wallpaper)


def delete_older_wallpapers(WALLPAPERS_LIST):
    wallpapers_list = os.listdir(WALLPAPER_FOLDER_PATH)

    # removing other files
    for index, wallpaper in enumerate(wallpapers_list):
        if wallpaper.endswith(".jpg") or wallpaper.endswith(".JPG"):
            if not wallpaper in WALLPAPERS_LIST:
                print(colored(f"Deleting {wallpaper}", "red"))
                os.remove(f'{WALLPAPER_FOLDER_PATH}/{wallpaper}')


def is_today_wallpaper_downloaded():
    """This function check whether today wallpaper already downloaded or not"""
    # Check whether today wallpaper downloaded or not
    with open(os.path.join(WALLPAPER_FOLDER_PATH, "current_wallpaper.txt")) as f:
        try:
            date_of_last_downloading = f.readlines()[1].strip()
        except:
            print(colored("DATE OF LAST DOWNLOADING NOT FOUND", "red"))
            return False

    today_date = datetime.datetime.now().strftime("%Y%m%d")

    return str(date_of_last_downloading) == str(today_date)


def update_data_in_record_file(string: str, line: int):
    """
    This function update data in record file Parameters
    -----------------------------
    string - Record to store line -
    line - number where record will store.
            1 for saving 'current wallpaper'.
            2 for saving 'last date of wallpaper downloaded'
    """
    with open(WALLPAPER_RECORD_FILE) as f:
        data = f.readlines()

    if len(data) != 2:
        with open(WALLPAPER_RECORD_FILE, "w") as f:
            f.write("current_wallpaper.png\ndownloaded_wallpaper_date")
        with open(WALLPAPER_RECORD_FILE) as f:
            data = f.readlines()

    data[line - 1] = string

    with open(WALLPAPER_RECORD_FILE, "w") as f:
        for i in data:
            if i.endswith("\n"):
                f.write(i)
            else:
                f.write(i + "\n")
