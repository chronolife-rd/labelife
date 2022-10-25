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

# Download
s_download = st.sidebar.empty()
# ------------- END BODY SIDEBAR

# ------------- BEGIN BODY  
# Start message
s_start_message = st.empty()

# Title
s_title = st.empty()

# Finish info
s_finish = st.empty()

# progress
s_progress_info = st.empty()
s_progress_bar  = st.empty()

# Columns
col1,col2,col3 = st.columns([6,1,2]) 

# Buttons
s_btn_first     = col2.empty() 
s_btn_last      = col3.empty()
s_btn_previous  = col2.empty() 
s_btn_next      = col3.empty()

# Radiobuttons
s_radiobtn      = col2.empty()
s_comment       = col2.empty()
s_btn_add_label = col2.empty()

# Image zone
s_image = col1.empty()

# Label info
s_label_info = st.empty()

# Posted message
s_post = col2.empty()
# ------------- END BODY

# ------------- BEGIN COMPLETE BODY
if username == '':
    s_start_message.title('Select a profile to start labeling')
    st.stop()
else:
    username = username.lower()

# s_title.title('Labelife')
btn_first       = s_btn_first.button('First') 
btn_last        = s_btn_last.button('Last')
btn_previous    = s_btn_previous.button('Previous') 
btn_next        = s_btn_next.button('Next')
quality         = s_radiobtn.radio("ECG Quality", QUALITY_OPTIONS)
btn_add_label   = s_btn_add_label.button('Add')
comment         = s_comment.text_area("Comments:", value="")
# ------------- END COMPLETE BODY  

# ------------- BEGIN GET DATA
data = get_data(PATH_DATA, username)
imax = len(data)
# ------------- END GET DATA


# ------------- BEGIN EVENTS
if btn_first:
    st.session_state['cnt'] = 1
    st.session_state['update'] = True

if btn_last:
    st.session_state['cnt'] = len(data)
    st.session_state['update'] = True

if btn_previous:
    if st.session_state['cnt'] > 1:
        st.session_state['cnt'] -= 1
    st.session_state['update'] = True

if btn_next:
    if st.session_state['cnt'] < imax:
        st.session_state['cnt'] += 1
    st.session_state['update'] = True

if btn_add_label:
    post_data(data, username, quality, comment, PATH_DATA)
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
    update_comment(s_comment, data, username, QUALITY_DICT)
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
