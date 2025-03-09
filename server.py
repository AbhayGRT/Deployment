import os
import streamlit as st
from datetime import datetime
from command import execute_command, execute_command_live, abort_process

output_areas = {}

def handle_server_side(s3Path, client, environment, ticket, serverEnv, developer):
    st.title("Server Side Deployment")
    st.divider()

    dev_paths = developer["users"][0]
    backup_folder = dev_paths['backup_folder_path']
    ticket_number = f"{client.upper()}-{ticket}" if ticket else f"server-{environment}-{client}-{datetime.now().strftime('%d-%m-%Y')}"
    full_path = os.path.join(dev_paths['backup_folder_path'])

    backup_path = os.path.join(backup_folder, ticket_number)
    os.makedirs(backup_path, exist_ok=True)

    build_command = f"cd {full_path} && rm -rf final-build && rm -rf final-build.tar.gz && npm run build"

    commands = {
        "1": {"label": "Server side Command (Tar file Backup)", "command": f"aws s3 cp {s3Path} {backup_path} --profile sportz", "lang": "bash"},
        "2": {"label": "Making Build", "command": build_command, "lang": "bash"},
        "3": {"label": "Deploying Tar File", "command": f"cd {full_path}/scripts/js && node create-server-build.js {client} {serverEnv}", "lang": "bash"}    }

    for key, cmd in commands.items():
        st.subheader(f"{key}. {cmd['label']}")
        st.code(cmd["command"], language=cmd["lang"])

        col1, col2 = st.columns(2)

        if key not in output_areas:
            output_areas[key] = st.empty()

        with col1:
            if st.button(f"Run {cmd['label']}", key=f"run_{key}"):
                if key == "2":
                    output = execute_command_live(cmd["command"], key,threshold=300)
                else:
                    output = execute_command(cmd["command"])
                
                output_areas[key].text_area(f"Output for {cmd['label']}:", output, height=150)

        with col2:
            if key == "2":
                if st.button(f"Abort {cmd['label']}", key=f"abort_{key}"):
                    abort_process(key)
                    st.warning(f"Process for {cmd['label']} aborted!")
