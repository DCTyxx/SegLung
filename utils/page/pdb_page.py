import streamlit as st
# from st_aggrid import AgGrid
import pandas as pd
import functools
from PIL import Image

def search_PDB():
    st.header('病例资料查看')
    with st.container():
        col1f, col2f, col3f = st.columns(3)
        # TODO 添加警告文件
        with col1f:
            st.text_input('Search for patients')
            st.button('search')

    # 个人信息查看框架
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            icon = st.image('C:\github\SegLung\img\person - 192x192.png', caption='avator')
            # TODO 使图像居中显示并且对齐
            st.button("change")
        with col2:
            st.write("名称")
            st.write("Uid")
            st.write("tel")
            st.write("password")
            # TODO 密码做不自动展示的动态
            # TODO 将用户信息链接进用户表中
            st.text_input('change your password', "password")
            st.button("submit")








