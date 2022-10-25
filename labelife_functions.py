import streamlit as st
from PIL import Image
from io import BytesIO
import pandas as pd
import time
import math

def restart_session():
    st.session_state['cnt'] = 1
    st.session_state['started'] = False

def init_session():
    # Session init
    st.set_page_config(layout="wide")
    
    if 'cnt' not in st.session_state:
        st.session_state['cnt'] = 1

    if 'started' not in st.session_state:
        st.session_state['started'] = False

    if 'update' not in st.session_state:
        st.session_state['update'] = False

    if 'post' not in st.session_state:
        st.session_state['post'] = False

def init_label(data, username):
    idx = data[data['label-' + username] == '-']['seg_id']
    if len(idx) > 0:
        idx = idx.iloc[0] 
    else:
        idx = len(data) 

    return idx

@st.cache
def convert_data_to_excel(data):
    # Cache the conversion to prevent computation on every rerun
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def clean_comment(s_comment):
    s_comment.text_area("Comments:", value="")

def get_data(PATH_DATA, username):
    data = pd.read_excel(PATH_DATA + 'data.xls')
    data = add_label_operator_column(data, username)
    data = add_comment_operator_column(data, username)

    return data

def get_image(PATH_IMAGE, data, username):
    # Find image not has_label
    if not st.session_state['started']:
        idx = init_label(data, username)
    else:
        idx = st.session_state['cnt']
    st.session_state['cnt'] = idx

    image = Image.open(PATH_IMAGE + str(idx) + '.jpg')
    return image, idx

def add_label_operator_column(data, username):
    if ('label-' + username) not in data.columns:
        data[('label-' + username)] = '-'
    return data

def add_comment_operator_column(data, username):
    if ('comment-' + username) not in data.columns:
        data[('comment-' + username)] = ''
    return data

def has_label(data, username, QUALITY_DICT):
    has_lab = False
    q = data.loc[st.session_state['cnt']-1, ('label-' + username)]
    if q != '-':
        has_lab = True
       
    return has_lab

def has_comment(data, username, QUALITY_DICT):
    has_com = False
    comment = data.loc[st.session_state['cnt']-1, ('comment-' + username)]
    if isinstance(comment, str):
        has_com = True
       
    return has_com

def post_data(data, username, quality, comment, PATH_DATA):
    data.loc[st.session_state['cnt']-1, ('label-' + username)] = quality
    data.loc[st.session_state['cnt']-1, ('comment-' + username)] = comment
    data.to_excel(PATH_DATA + 'data.xls', index=False)      

# def update_quality_radiobutton(s_radiobtn, data, username, QUALITY_DICT, QUALITY_OPTIONS):
#     if has_label(data, username, QUALITY_DICT):
#         q = data.loc[st.session_state['cnt']-1, ('label-' + username)]
#         if QUALITY_DICT[q] > 0:
#             s_radiobtn.empty()
#             s_radiobtn.radio("ECG Quality", QUALITY_OPTIONS, QUALITY_DICT[q])
    
def update_label_info(s_label_info, data, username, QUALITY_DICT):
    if has_label(data, username, QUALITY_DICT):
        q = data.loc[st.session_state['cnt']-1, ('label-' + username)]
        s_label_info.empty()
        s_label_info.info('Label: ' + q)  

def update_comment_info(s_comment_info, s_comment, data, username, QUALITY_DICT):
    if has_comment(data, username, QUALITY_DICT):
        comment = data.loc[st.session_state['cnt']-1, ('comment-' + username)]
        s_comment_info.empty()
        s_comment_info.warning("Comment: " + comment)

# def init_comment(s_comment):
#     s_comment.empty()
#     s_comment.text_area("Comment:", value=" ")

def update_image(PATH_IMAGE, data, username, s_image):
    image, idx  = get_image('PATH_IMAGE', data, username)
    s_image.image(image, caption='ECG')

def update_progress(PATH_IMAGE, data, username, s_image, s_progress_info, s_progress_bar):
    idx = st.session_state['cnt'] 
    progress    = str(idx) + '/' + str(len(data))
    s_progress_info.text(progress)
    my_bar      = s_progress_bar.progress(idx/len(data))

def update_finish_message(s_finish, data, username):
    # Finish message
    idx = data[data['label-' + username] == '-']['seg_id']
    if len(idx) == 0:
        s_finish.success('Congrats! you have annotated all images')
        st.balloons()

def update_download(data, s_download):
    # download
    excel = convert_data_to_excel(data)

    s_download.download_button(
        label="Download",
        data=excel,
        file_name='data_label.xlsx',
    )
    
def display_post_message(s_post, quality):
    s_post.success('"' + quality + '" label added')
    
def hide_post_message(s_post):
    if st.session_state['post']:
        time.sleep(1)
        s_post.empty()
    st.session_state['post'] = False

    
