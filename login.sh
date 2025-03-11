#!/bin/bash

DATA_FILE="data.json"

# Function to prompt user for input
get_user_input() {
    echo "Enter Name: "
    read name
    echo "Enter WAF folder path: "
    read waf_folder_path
    echo "Enter Upload folder path: "
    read build_folder_path
    echo "Enter Backup folder path: "
    read backup_folder_path
    echo "Enter Custom Video Url: "
    read custom_video
}

# Function to update or create the JSON file
update_json_file() {
    if [ ! -f "$DATA_FILE" ]; then
        echo '{"users": []}' > "$DATA_FILE"
    fi

    # Read the existing JSON data
    json_data=$(cat "$DATA_FILE")

    # Create user JSON object
    new_user=$(jq -n \
        --arg name "$name" \
        --arg waf_folder_path "$waf_folder_path" \
        --arg build_folder_path "$build_folder_path" \
        --arg backup_folder_path "$backup_folder_path" \
        --arg custom_video "$custom_video" \
        '{name: $name, waf_folder_path: $waf_folder_path, build_folder_path: $build_folder_path, backup_folder_path: $backup_folder_path, custom_video: $custom_video}')

    # Append new user data to users array
    updated_json=$(echo "$json_data" | jq --argjson new_user "$new_user" '.users += [$new_user]')

    # Save updated JSON back to file
    echo "$updated_json" > "$DATA_FILE"
    echo "User data saved successfully."
}

# Main execution
get_user_input
update_json_file
