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
        f.write("defualt.png")
with open(WALLPAPER_RECORD_FILE) as f:
    CURRENT_WALLPAPER = f.readline()


def download():
    api_url = "https://bing.biturl.top/?resolution=1920&format=json&index=0&mkt=zh-CN"

    print("-------Connecting to server-------")
    n = 0
    while True:
        try:
            response = requests.get(api_url)
            break
        except Exception:
            n += 1
            if n == 1:
                print(colored("\n------ Make Sure you are connected to internet  ------.", "red"))
            if n == 50:
                print(colored("------ Cannot able to make connection with server ------", "red"))
                input("Press any key to exit..... ")
                exit()
    os.system("clear")
    print(colored("\n------ SERVER CONNECTION SUCESSFUL ------)", "green"))

    # Making list from json response
    response = json.loads(response.text)

    print(colored("\n------ DOWNLOADING WALLPAPER ------\n", "blue"))
    wallpaper_file_name = response['start_date'] + ".jpg"

    # check if wallpaper already exists
    global WALLPAPER_FOLDER_PATH
    if os.path.isfile(f'{WALLPAPER_FOLDER_PATH}/{wallpaper_file_name}'):
        print(colored("\n------ WALLPAPER ALREADY EXISTS ------", "red"))
        return wallpaper_file_name

    # Downloading the wallpaper
    with requests.get(response["url"], stream=True) as r:
        r.raise_for_status()
        with open(f'{WALLPAPER_FOLDER_PATH}/{wallpaper_file_name}', "wb") as image_file:
            for chunk in tqdm(r.iter_content(chunk_size=1024)):
                image_file.write(chunk)
                image_file.flush()

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

    with open(WALLPAPER_RECORD_FILE, "w") as f:
        f.write(wallpaper_file_name)


def set_random():
    wallpapers = os.listdir(WALLPAPER_FOLDER_PATH)
    wallpaper = wallpapers[random.randint(0, len(wallpapers) - 1)]
    set_wallpaper(wallpaper)


def set_next_wallpaper(previous=False):
    if not os.path.isfile(WALLPAPER_RECORD_FILE):
        print(colored("CURRENT WALLPAPER DOES NOT EXIST", "red"))
        set_latest_wallpaper()
        return

    with open(WALLPAPER_RECORD_FILE) as f:
        current_wallpaper = f.readline()

    if current_wallpaper == "":
        print(colored("CURRENT WALLPAPER DOES NOT EXIST", "red"))
        set_latest_wallpaper()
        return

    wallpapers_list = os.listdir(WALLPAPER_FOLDER_PATH)

    # removing other files
    for index, wallpaper in enumerate(wallpapers_list):
        if not wallpaper.endswith(".jpg") or wallpaper.endswith(".JPG"):
            wallpapers_list.pop(index)

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

    if len(wallpapers_list) > 0:
        set_wallpaper(wallpapers_list[0])
    else:
        print(colored("THERE IS NO DOWNLOADED WALLPAPER", "blue"))
