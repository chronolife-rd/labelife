import streamlit as st
import random

import pandas as pd
import numpy as np

from constant import QUALITY_DICT, QUALITY_OPTIONS, PATH_DATA, PATH_IMAGE,\
                    MESSAGE_USER_SLECTION, USERNAMES
from labelife_functions import *

init_session()

# ------------- BEGIN BODY SIDEBAR
username = st.sidebar.selectbox(MESSAGE_USER_SLECTION, USERNAMES, key='username', on_change=restart_session)

if username == '':
    st.stop()
else:
    username = username.lower()

# Download
s_download = st.sidebar.empty()
# ------------- END BODY SIDEBAR

# ------------- BEGIN GET DATA
data = get_data(PATH_DATA, username)
imax = len(data)
# ------------- END GET DATA

# ------------- BEGIN BODY  
# Title
s_title = st.empty()
s_title.title('Labelife')

# Finish info
s_finish = st.empty()

# progress
s_progress_info = st.empty()
s_progress_bar  = st.empty()

# Columns
col1,col2,col3 = st.columns([6,1,2]) 

# Buttons
s_btn_previous  = col2.empty() 
s_btn_next      = col3.empty()
btn_previous    = s_btn_previous.button('Previous') 
btn_next        = s_btn_next.button('Next')

# Radiobuttons
s_radiobtn      = col2.empty()
s_btn_add_label = col2.empty()
quality         = s_radiobtn.radio("ECG Quality", QUALITY_OPTIONS)
btn_add_label   = s_btn_add_label.button('Add')

# Image zone
s_image = col1.empty()

# Label info
s_label_info = st.empty()

# Posted message
s_post = st.empty()
# ------------- END BODY

# ------------- BEGIN EVENTS
if btn_previous:
    if st.session_state['cnt'] > 1:
        st.session_state['cnt'] -= 1
    st.session_state['update'] = True

if btn_next:
    if st.session_state['cnt'] < imax:
        st.session_state['cnt'] += 1
    st.session_state['update'] = True

if btn_add_label:
    post_label(data, username, quality, PATH_DATA)
    if st.session_state['cnt'] < imax:
        st.session_state['cnt'] += 1
    st.session_state['update'] = True
    st.session_state['post'] = True
    # check finish 
    display_post_message(s_post, quality)
    update_finish_message(s_finish, data, username)

if st.session_state['update']:
    update_quality_radiobutton(s_radiobtn, data, username, QUALITY_DICT, QUALITY_OPTIONS)
    update_label_info(s_label_info, data, username, QUALITY_DICT)
    st.session_state['update'] = False
    
# ------------- END EVENTS

# Update image 
update_image(PATH_IMAGE, data, username, s_image)
# update progress bar
update_progress(PATH_IMAGE, data, username, s_image, s_progress_info, s_progress_bar)
# update download
update_download(data, s_download)
# Hide post message
hide_post_message(s_post)

# Session start update
st.session_state['started'] = True
st.session_state['post'] = False
