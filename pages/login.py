import streamlit as st
import json
import os

DATA_FILE = "data.json"

def load_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                return data.get("users", [])
        except json.JSONDecodeError:
            return []
    return []

def save_user_data(user_data):
    with open(DATA_FILE, "w") as file:
        json.dump({"users": [user_data]}, file, indent=2)

st.title("User Profile")

users = load_user_data()
user = users[0] if users else {}

name = st.text_input("Enter Name:", user.get("name", ""))
waf_folder_path = st.text_input("Enter WAF Folder Path:", user.get("waf_folder_path", ""))
build_folder_path = st.text_input("Enter Upload Folder Path:", user.get("build_folder_path", ""))
backup_folder_path = st.text_input("Enter Backup Folder Path:", user.get("backup_folder_path", ""))
custom_video = st.text_input("Enter Custom Video URL:", user.get("custom_video", ""))

if st.button("Submit"):
    user_data = {
        "name": name,
        "waf_folder_path": waf_folder_path,
        "build_folder_path": build_folder_path,
        "backup_folder_path": backup_folder_path,
        "custom_video": custom_video
    }
    save_user_data(user_data)
    st.success("Profile saved successfully! Redirecting to Home...")
    st.switch_page("streamlit.py")
