import streamlit as st
from main import getDeveloper,initialize_json,update_media_state

def handle_media(customVideo,fallbackImage):
    initialize_json()

    data = getDeveloper()
    initial_state = data["media_handle"]

    media_toggle = st.toggle(" ", value=initial_state)

    if media_toggle != initial_state:
        update_media_state(media_toggle)

    if media_toggle:
        st.video(customVideo)
    else:
        st.image(fallbackImage, use_container_width=True)
