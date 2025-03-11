import streamlit as st
from main import *
from server import handle_server_side
from client import handle_client_side
from media import handle_media

st.set_page_config(page_title="Deployment", layout="wide")

loadCSS("style.css")

if not check_user_setup():
    st.switch_page("pages/login.py")

makhachev = getMakhachev()
clients = makhachev.get("clients", [])
environments = makhachev.get("environments", [])
serverStg = makhachev.get("server_stg", {})
serverProd = makhachev.get("server_prod", {})
stgBeta = makhachev.get("stg_beta", "")
stgProd = makhachev.get("stg_prod", "")
clientStg = makhachev.get("client_stg", {})
clientProd = makhachev.get("client_prod", {})
branch = makhachev.get("branch", {})
fallbackImage = makhachev.get("fallback_image","")

developer = getDeveloper()

with st.sidebar:
    st.header("Inputs")
    
    st.divider()

    selectedClient = st.selectbox("Select Client: ", clients)
    selectedEnvironments = st.selectbox("Select Environment: ", environments)
    ticketNumber = st.text_input("Enter Ticket No (eg: 1636): ")
    

    getBranchData = getBranch(selectedClient, selectedEnvironments, branch, developer["users"][0]['waf_folder_path'])
    customBranch = False 

    if not getBranchData:
        st.divider()
        current_branch = getBranchName(developer["users"][0]['waf_folder_path'])
        st.warning(f"Current branch: `{current_branch}` is not valid for deployment.")
        
        custom_branch_toggle = st.toggle("Using a custom branch")
        if custom_branch_toggle:
            customBranch = True
    
    st.divider()

    if customBranch or getBranchData:
        deploymentTypeToggle = st.toggle("Switch Environment Type", value=False)
        deploymentType = "Server Side" if deploymentTypeToggle else "Client Side"
    else:
        deploymentType = "Client Side"


if deploymentType == "Server Side" and (getBranchData or customBranch):
    if selectedEnvironments == "stg":
        serverEnv = stgBeta
        s3Path = serverStg[selectedClient]
    else:
        serverEnv = stgProd
        s3Path = serverProd[selectedClient]
    handle_server_side(s3Path, selectedClient, selectedEnvironments, ticketNumber, serverEnv, developer)

elif deploymentType == "Client Side" and (getBranchData or customBranch):
    if selectedEnvironments == "stg":
        s3Path = clientStg[selectedClient]
    else:
        s3Path = clientProd[selectedClient]
    handle_client_side(s3Path, selectedClient, selectedEnvironments, ticketNumber, developer)

else:
    handle_media(developer["users"][0]['custom_video'],fallbackImage)

    