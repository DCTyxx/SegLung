import streamlit as st
import numpy as np
from ..data.readUserList import read
import os


def login():
    st.sidebar.markdown("## Log In")
    uid = st.sidebar.text_input(label='账号', placeholder="Uid")
    password = st.sidebar.text_input(label='密码', placeholder="password",type="password")
    if st.sidebar.button("login"):
        path = os.getcwd()  # 获取当前路径

        path = os.path.join("./utils/page/userList.csv")
        if read(file=path, name=uid) == password:
            flag = 1


    cont1 = st.sidebar.container()

    with cont1:
        col1, col2= st.sidebar.columns(2)
        with cont1:
            st.sidebar.write("forget your password?")
        with col2:
            st.sidebar.button("find")





