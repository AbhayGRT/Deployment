#!/bin/bash

cd ~/Deployment

JSON_FILE="data.json"

WAF_FOLDER_PATH=$(jq -r '.users[0].waf_folder_path' "$JSON_FILE")
BACKUP_FOLDER_PATH=$(jq -r '.users[0].backup_folder_path' "$JSON_FILE")

# Check if the waf folder path exists
if [ -d "$WAF_FOLDER_PATH" ]; then
    gnome-terminal --working-directory="$WAF_FOLDER_PATH" --maximize
    find "$BACKUP_FOLDER_PATH" -mindepth 1 -type d -empty -exec rm -rf {} \;
else
    echo "Error: Directory '$WAF_FOLDER_PATH' does not exist."
fi
