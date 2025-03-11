import requests
import json
from command import get_current_git_branch
import os
import streamlit as st

def getMakhachev():
    """ Fetches data from an API """
    try:
        response = requests.get("https://makhachev.vercel.app/")
        data = response.json()
        # print(json.dumps(data, indent=4))
        return data
    except requests.RequestException as e:
        print(f"Error fetching API data: {e}")
    except Exception as e:
        print(f"getMakhachev: {e}")

def getDeveloper():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            # print(data["users"][0]["name"])
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading data.json: {str(e)}")
    except Exception as e:
        print(f"getDeveloper: {e}")

def getBranch(client,environment,branch,folderPath):
    index = 0 if environment == "stg" else 1
    if branch[client][index] == get_current_git_branch(folderPath):
        return True
    else:
        return False
    
def getBranchName(folderPath):
    return get_current_git_branch(folderPath)

def update_media_state(media_state):
    data = getDeveloper()
    data["media_handle"] = media_state

    with open('data.json', "w") as file:
        json.dump(data, file, indent=4)
        
def initialize_json():
    if not os.path.exists('data.json'):
        with open('data.json', "w") as file:
            json.dump({"media_handle": False}, file, indent=4)
    else:
        with open('data.json', "r+") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
                
            if "media_handle" not in data:
                data["media_handle"] = False
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

def loadCSS(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        

def load_json_file(file_path):
    """Load JSON data from a file if it exists, otherwise return an empty dictionary."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            content = file.read().strip()
            if content:
                return json.loads(content)
    return {}


def check_user_setup():
    data = load_json_file("data.json")
    if "users" in data and data["users"]:
        return True
    return False