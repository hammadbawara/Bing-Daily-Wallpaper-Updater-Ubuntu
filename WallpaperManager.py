import requests
import json
import os
from tqdm import tqdm
from termcolor import colored
import random

# Global Variables
FOLDER_NAME = "wallpapers"

if not os.path.isdir(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)


def download():
    api_url = "https://bing.biturl.top/?resolution=1920&format=json&index=0&mkt=zh-CN"

    print("-------Connecting to server-------")
    n = 0
    while True:
        try:
            response = requests.get(api_url)
            break
        except Exception as e:
            n+=1
            if (n==1):
                print(colored("\n------ Make Sure you are connected to internet  ------.", "red"))
            if (n==50):
                print(colored("------ Cannot able to make connection with server ------", "red"))
                input("Press any key to exit..... ")
                exit()
    os.system("clear")
    print(colored("\n------ SERVER CONNECTION SUCESSFUL ------)", "green"))
                

    # Making list from json response
    response = json.loads(response.text)

    print(colored("\n------ DOWNLOADING WALLPAPER ------\n", "blue"))
    wallpaper_file_name = response['start_date'] + ".jpg"

    #check if wallpaper already exists
    global FOLDER_NAME
    if os.path.isfile(f'{FOLDER_NAME}/{wallpaper_file_name}'):
        print(colored("\n------ WALLPAPER ALREADY EXISTS ------", "red"))
        return wallpaper_file_name
    
    # Downloading the wallpaper
    with requests.get(response["url"], stream=True) as r:
        r.raise_for_status()
        with open (f'{FOLDER_NAME}/{wallpaper_file_name}', "wb") as image_file:
            for chunk in tqdm(r.iter_content(chunk_size=1024)):
                image_file.write(chunk)
                image_file.flush()

    print(colored("\n------ WALLPAPER DOWNLOADED ------", "green"))

    return wallpaper_file_name

def set_wallpaper(wallpaper_file_name : str):
    os.system(f"gsettings set org.gnome.desktop.background picture-uri 'file://{os.getcwd()}/{FOLDER_NAME}/{wallpaper_file_name}'")
    print(colored("\n------ WALLPAPER SET ------", "green"))

def set_random():
    wallpapers = os.listdir(FOLDER_NAME)
    wallpaper = wallpapers[random.randint(0, len(wallpapers)-1)]
    set_wallpaper(wallpaper)
    
