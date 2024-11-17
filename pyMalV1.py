import os
import time
import datetime

base_directory = "D:\\OS PROJECT\\malActDir"

if not os.path.exists(base_directory):
    os.mkdir(base_directory)


def create_folder_with_file():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join(base_directory, f"Folder_{timestamp}")
    os.mkdir(folder_path)
    with open(os.path.join(folder_path, "info.txt"), "w") as file:
        file.write(f"This file was created on {timestamp}")
    print(f"Created folder: {folder_path} with a file inside.")


try:
    while True:
        create_folder_with_file()
        time.sleep(5)
except KeyboardInterrupt:
    print("Program stopped by the user.")