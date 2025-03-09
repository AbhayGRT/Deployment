import subprocess
import time
import streamlit as st

processes = {}

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def execute_command_live(command, key,threshold=300):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes[key] = process
    
    output_area = st.empty()
    start_time = time.time()
    output_lines = []
    for line in process.stdout:
        output_lines.append(line.strip())
        output_area.text_area("Live Output:", "\n".join(output_lines), height=200)
        
        if time.time() - start_time > threshold:
            process.terminate()
            processes.pop(key, None)
            return f"Process aborted automatically after {threshold} seconds!"
    
    process.wait()
    processes.pop(key, None)
    return "\n".join(output_lines) if output_lines else process.stderr.read()

def abort_process(key):
    if key in processes:
        processes[key].terminate()
        del processes[key]

def get_current_git_branch(folderPath):
    """
    Get the current Git branch using git command.
    Returns: str: The current Git branch name.
    """
    try:
        result = subprocess.run(
            ["git", "-C", folderPath, "rev-parse", "--abbrev-ref", "HEAD"],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print("Error getting current git branch:", e)
        return None