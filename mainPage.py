import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import streamlit as st
from PIL import Image
from utils.data.readUserList import read
import os
from utils.page.segmentation import mainboard
from utils.page.pdb_page import search_PDB
import cv2 as cv



class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        nowFile = os.getcwd()
        posterFile = os.path.join(nowFile,"poster/poster_page-0001.jpg")
        # poster = open(posterFile,encoding='utf-8').read()
        poster = cv.imread(posterFile)
        poster = cv.cvtColor(poster,cv.COLOR_BGR2RGB)

        img = Image.open(
            r"./img/person - 192x192.png"
        )

        st.set_page_config(page_title="SegLung",
                           page_icon=img,
                           layout="wide",
                           initial_sidebar_state="auto"
                           )
        placeholder = st.sidebar.empty()
        with placeholder.container():
            st.markdown("## Log In")
            uid = st.text_input(label='User ID', placeholder="Uid")
            password = st.text_input(label='Password', placeholder="password", type="password")
            st.markdown("---")

        placeholder3 = st.empty()
        with placeholder3.container():
            st.image(poster)
            # st.latex(poster)



        path = os.path.join("./UserData/userList.csv")
        passw,job,PatientsID = read(file=path, name=uid)
        if passw == password:
            placeholder.empty()
            placeholder3.empty()
            st.sidebar.markdown('## Wellcome Back ' + PatientsID + ' , Have a Nice Day!')
            st.sidebar.markdown("---")
            st.markdown("## Main Menu")
            appx = st.sidebar.selectbox(
                "Select Page", self.apps, format_func=lambda app: app["title"]
            )
            st.sidebar.markdown("---")
            appx["function"](job,nowFile,PatientsID)



app = MultiApp()

app.add_app("Segmentation", mainboard)
# app.add_app("Database Overview", overview_page)
app.add_app("Search PDB", search_PDB)
# app.add_app("Explore Conformations", conformation_page)
# app.add_app("Analyze Mutations", mutation_page)
# app.add_app("Compare Inhibitors", inhibitor_page)
# app.add_app("Query Database", query_page)
# app.add_app("Classify Structures", classify_page)

app.run()