from ctypes import windll
from comtypes import CLSCTX_ALL
import pystray
import threading
import psutil
import time
from PIL import Image
import shutil
import glob
import random
import os
def check_path_type(path):
    if os.path.isfile(path):
        return "File"
    elif os.path.isdir(path):
        return "Folder"
    else:
        return "Path does not exist or is neither a file nor a folder."
def is_process_running():
    """Check if a process is running."""
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == _process_name:
            return True
    return False
def get_random_mp4(folder_path):
    # Construct the search pattern
    search_pattern = f"{folder_path}/*.mp4"
    # Find all .mp4 files in the folder
    mp4_files = glob.glob(search_pattern)    
    # Select one at random if any are found
    if mp4_files:
        return random.choice(mp4_files)
    else:
        return None  # Or handle the case where no .mp4 files are found as needed
def monitor_process():
    """Monitor if a process starts running, checking every 'interval' seconds."""
    while not exit_event.is_set():
        if is_process_running():
            print(f"{_process_name} has started.")
            if False == _isFolder:
                try:
                    shutil.copy2(_homevideo, _filename)
                    print(f"Selected: {_homevideo}")
                except Exception as e:
                    print(f"Error: {e}")
                    pass
            else:
                try:
                    test = get_random_mp4(_homevideo)
                    print(f"Selected: {test}")
                    shutil.copy2(test, _filename)
                except Exception as e:
                    print(f"Error: {e}")
                    pass
             # Exit the loop if the process is found
        time.sleep(float(_change_interval))
def on_exit(icon, item):
    icon.stop()
    exit_event.set()
    monitor_thread.join()
def refresh_settings(icon, item):        
    read_settings()
def setup_tray_icon():    
    menu = pystray.Menu(
        pystray.MenuItem('Refresh settings', refresh_settings),
        pystray.MenuItem('Exit', on_exit)
    )
    icon = pystray.Icon("ValorantHomePageChanger", Image.open("icon.png"), "Valorant HomePage Changer", menu)
    icon.run()
def read_settings():
    try:
        monitor_thread.join()
    except:
        pass
    global _homevideo, _valid, _change_interval, _process_name, _filename, _isFolder
    with open("settings.txt", "r") as settings_file:
        settings = settings_file.readlines()
        _homevideo = settings[0].strip()
        if check_path_type(_homevideo) == "Folder":
            _valid = True
            _isFolder = True
        elif _homevideo.endswith(".mp4"):
            _valid = True
            _isFolder = False
        else:
            _valid = False
            _isFolder = False
        _change_interval = settings[1].strip()   
        _filename = settings[2].strip()     
        _process_name = "VALORANT.exe"
    monitor_thread = threading.Thread(target=monitor_process)
    monitor_thread.start()

exit_event = threading.Event()
monitor_thread = threading.Thread(target=monitor_process)
def main():
    read_settings()
    print(f"Default homevideo: {_filename}")
    print(f"Desired Homevideo: {_homevideo}")
    print(f"Valid: {_valid}")
    print(f"Process name: {_process_name}")
    print(f"Change interval: {_change_interval}")
    print(f"Is folder: {_isFolder}")

    
    # Start the tray icon
    setup_tray_icon()

if __name__ == "__main__":
    main()
