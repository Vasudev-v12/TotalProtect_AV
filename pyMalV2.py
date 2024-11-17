import os
import time
from datetime import datetime

base_directory = "D:\\OS PROJECT\\malActDir"

os.makedirs(base_directory, exist_ok=True)

try:
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_folder_path = os.path.join(base_directory, f"Folder_{current_time}")
        os.makedirs(new_folder_path, exist_ok=True)
        file_path = os.path.join(new_folder_path, "info.txt")
        with open(file_path, "w") as file:
            file.write(f"This file was created on {datetime.now().isoformat()}")
        print(f"Created folder: {new_folder_path} with a file inside it.")        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("Program stopped by the user.")