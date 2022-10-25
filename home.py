import streamlit as st
import random

import pandas as pd
import numpy as np

from constant import QUALITY_DICT, QUALITY_OPTIONS, PATH_DATA, PATH_IMAGE,\
                    MESSAGE_USER_SLECTION, USERNAMES
from labelife_functions import *

init_session()

# Start message
s_start_message = st.empty()

# ------------- BEGIN BODY 
# Profile
profile = st.sidebar.selectbox(MESSAGE_USER_SLECTION, USERNAMES, key='profile', on_change=restart_session)
st.sidebar.markdown('#') # Space

if profile == '':
    s_start_message.title('Select a profile to start labeling')
    st.stop()
else:
    username = profile.lower()

# Radiobuttons
with st.sidebar.form("my_form"):
    s_radiobtn      = st.empty()
    s_comment       = st.empty()
    btn_add         = st.form_submit_button('Add')

# Posted message
s_post = st.sidebar.empty()

# Download
st.sidebar.markdown('#') # Space
st.sidebar.write('Download labels')
s_download = st.sidebar.empty()

# Title
s_title = st.empty()

# Finish info
s_finish = st.empty()

# progress
s_progress_info = st.empty()
s_progress_bar  = st.empty()

# Navigation
_, c_nav1, c_nav2, c_nav3, c_nav4, _= st.columns([6,1,1,1,1,6]) 
s_btn_first     = c_nav1.empty() 
s_btn_previous  = c_nav2.empty() 
s_btn_next      = c_nav3.empty()
s_btn_last      = c_nav4.empty()

_,col_img,_,= st.columns([1,5,1]) 
# Label info
s_label_info = col_img.empty()
# Comment info
s_comment_info = col_img.empty()

# Image zone
s_image = col_img.empty()
# ------------- END BODY

# ------------- BEGIN COMPLETE BODY
# s_title.title('Labelife')
btn_first       = s_btn_first.button('First') 
btn_last        = s_btn_last.button('Last')
btn_previous    = s_btn_previous.button('Previous') 
btn_next        = s_btn_next.button('Next')
quality         = s_radiobtn.radio("ECG Quality", QUALITY_OPTIONS)
comment         = s_comment.text_area("Comment:", value="")

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

if btn_add:
    post_data(data, username, quality, comment, PATH_DATA)
    
    if st.session_state['cnt'] < imax:
        st.session_state['cnt'] += 1
    st.session_state['update'] = True
    st.session_state['post'] = True

if st.session_state['update']:
    update_label_info(s_label_info, data, username, QUALITY_DICT)
    update_comment_info(s_comment_info, s_comment, data, username, QUALITY_DICT)
    st.session_state['update'] = False

if st.session_state['post']:
    # check finish 
    display_post_message(s_post, quality)
    update_finish_message(s_finish, data, username)

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
