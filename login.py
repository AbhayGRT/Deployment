import json
import os

def get_user_input():
    """Prompt the user for required inputs."""
    user_data = {
        "name": input("Enter Name: ").strip(),
        "waf_folder_path": input("Enter WAF folder path: ").strip(),
        "build_folder_path": input("Enter Upload folder path: ").strip(),
        "backup_folder_path": input("Enter Backup folder path: ").strip(),
        "custom_video": input("Enter Custom Video Url: ").strip(),
    }
    return user_data

def load_json_file(file_path):
    """Load JSON data from a file if it exists, otherwise return an empty dictionary."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

def save_json_file(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def update_json_file():
    DATA_FILE = "data.json"
    """Update or create the data.json file with user inputs."""
    data = load_json_file(DATA_FILE)

    if "users" not in data:
        data["users"] = []

    user_data = get_user_input()

    data["users"].append(user_data)

    save_json_file(DATA_FILE, data)
    print(f"User data saved successfully")
    
    
update_json_file()
