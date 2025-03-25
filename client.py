import streamlit as st
from datetime import datetime
import os
import re
from command import execute_command
import shutil

def handle_client_side(s3Path, client, environment, ticket, developer):
    st.title("Client Side Deployment")

    dev_paths = developer["users"][0]
    full_path = os.path.join(dev_paths['waf_folder_path'], 'dist', client, 'client-build', 'development')
    upload_folder = dev_paths['build_folder_path']
    backup_folder = dev_paths['backup_folder_path']

    ticket_number = f"{client.upper()}-{ticket}" if ticket else f"client-{environment}-{client}-{datetime.now().strftime('%d-%m-%Y')}"

    if not os.path.exists(full_path):
        st.error(f"Build path {full_path} does not exist. Please check the path and client selection.")
        return

    build_files = os.listdir(full_path)

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = set()

    existing_uploads = os.listdir(upload_folder) if os.path.exists(upload_folder) else []
    if existing_uploads:
        st.warning("Before selecting files, all previous files in the upload folder will be deleted.")
        if st.button("Click here to clear upload folder before selecting files"):
            for file in existing_uploads:
                try:
                    os.remove(os.path.join(upload_folder, file))
                except Exception as e:
                    st.error(f"Failed to delete {file}: {str(e)}")
            st.success("Upload folder cleared! You can now select files.")

    st.divider()

    selected_files = st.multiselect("Select files to upload", build_files, key="file_selection")

    uploaded_files = st.session_state["uploaded_files"]
    deselected_files = uploaded_files - set(selected_files)

    for file in deselected_files:
        try:
            os.remove(os.path.join(upload_folder, file))
            st.success(f"Removed {file} from the upload folder.")
        except FileNotFoundError:
            pass

    st.session_state["uploaded_files"] = set(selected_files)

    if selected_files:
        os.makedirs(upload_folder, exist_ok=True)
        for file in selected_files:
            if file not in uploaded_files:
                try:
                    shutil.copy(os.path.join(full_path, file), os.path.join(upload_folder, file))
                    st.success(f"Copied {file} to upload folder.")
                except Exception as e:
                    st.error(f"Failed to copy file: {file}. Error: {str(e)}")

    st.divider()

    backup_path = os.path.join(backup_folder, ticket_number)
    os.makedirs(backup_path, exist_ok=True)

    includes = " ".join([f'--include \"{file}\"' for file in selected_files]) if selected_files else ""
    backup_command = f"aws s3 cp {s3Path} {backup_path} --recursive --profile sportz --exclude \"*\" {includes}"
    upload_command = f"aws s3 cp {upload_folder} {s3Path} --recursive --profile sportz"

    grep_pattern = ""
    if selected_files:
        escaped_files = [re.escape(file) + "$" for file in selected_files]
        grep_pattern = f" | grep -E '{'|'.join(escaped_files)}'"
        
    st.session_state["output"] = {
        "1": {"label": "Backup Command", "command": backup_command, "lang": "bash"},
        "2": {"label": "Dry Run Command", "command": f"{upload_command} --dryrun", "lang": "bash"},
        "3": {"label": "Upload Command", "command": upload_command, "lang": "bash"},
        "4": {"label": "Check Command", "command": f"aws s3 ls {s3Path.rstrip('/')}/ --profile sportz {grep_pattern}", "lang": "bash"},
    }

    for key, cmd in st.session_state["output"].items():
        st.subheader(f"{key}. {cmd['label']}")
        st.code(cmd["command"], language=cmd["lang"])

        if key == "3":
            # print("selected_files",selected_files)
            if st.button("Prepare to Upload"):
                st.session_state["show_confirmation"] = True

            if st.session_state.get("show_confirmation", False):
                st.write("### Files to be uploaded:",selected_files)
                # st.write("\n".join(selected_files))

                confirm = st.radio("Are you sure you want to upload these files?", ("No", "Yes"), key="upload_confirm")
                if confirm == "Yes":
                    output = execute_command(upload_command)
                    st.text_area("Upload Output:", output, height=150)
                    st.session_state["show_confirmation"] = False

        else:
            if st.button(f"Run {cmd['label']}"):
                output = execute_command(cmd["command"])
                st.text_area("Output:", output, height=150)
