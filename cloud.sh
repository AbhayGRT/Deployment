#!/bin/bash

# Define the script path for the new shortcut (Alt + A)
RUN_SCRIPT_PATH="$(realpath deployment.sh)"

# Ensure the script exists
if [ ! -f "$RUN_SCRIPT_PATH" ]; then
    echo "Error: Script $RUN_SCRIPT_PATH not found!"
    exit 1
fi

echo "Fetching existing custom shortcuts..."
EXISTING_SHORTCUTS=$(gsettings get org.gnome.settings-daemon.plugins.media-keys custom-keybindings)

# Convert to a valid format
if [ "$EXISTING_SHORTCUTS" == "@as []" ]; then
    # If no shortcuts exist, initialize the list with custom0
    NEW_SHORTCUTS="['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"
    SHORTCUT_INDEX=0
else
    # Extract customX numbers, find the highest index, and add a new one
    LAST_INDEX=$(echo "$EXISTING_SHORTCUTS" | grep -o "custom[0-9]*" | sed 's/custom//' | sort -n | tail -1)
    if [ -z "$LAST_INDEX" ]; then
        SHORTCUT_INDEX=0
    else
        SHORTCUT_INDEX=$((LAST_INDEX + 1))
    fi
    NEW_SHORTCUTS=$(echo "$EXISTING_SHORTCUTS" | sed "s/]$/, '\/org\/gnome\/settings-daemon\/plugins\/media-keys\/custom-keybindings\/custom$SHORTCUT_INDEX\/']/")
fi

echo "Adding new shortcut at index $SHORTCUT_INDEX..."

# Update the list of custom shortcuts
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "$NEW_SHORTCUTS"

# Define the new shortcut (customX)
CUSTOM_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$SHORTCUT_INDEX/"

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$CUSTOM_PATH name "Makhachev"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$CUSTOM_PATH command "$RUN_SCRIPT_PATH"
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$CUSTOM_PATH binding "<Alt>A"

echo "Shortcut Alt + A assigned to $RUN_SCRIPT_PATH without affecting previous shortcuts!"
