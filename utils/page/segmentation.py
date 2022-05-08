import os.path

import streamlit as st
import cv2 as cv
from ..juxtapose.Use import juxtapose
from ..data import loadPatients
from ..model.InfNet import InfNetpredict
from ..model.UNet import UNetpredict
from ..model.DeepLabV3Plus import DeeplabV3Ppredict
from ..model.All import All


def mainboard(UserName):

    file = r"./parametersData/LungSlides"
    saveRoot = r'./result/ModelResult'
    listFile = []
    patientsInfo = {}
    optionx = "option"
    Network = [
        {"title": "InfNet", "function": InfNetpredict},
        {"title": "DeepLabV3+", "function": DeeplabV3Ppredict},
        {"title": "UNet", "function": UNetpredict},
        # {"title": "All", "function": All}
    ]
    # sidebar
    st.sidebar.markdown("## Neural Network Menu")
    network = st.sidebar.selectbox(
                "Neural Network", Network,format_func=lambda net: net["title"]
            )

    genre = st.sidebar.radio(
        label="Select the view",
        options=('Traditional', 'Super View'),
        index=0
    )



    # 主面板界面

    with st.container():
        col1c, col2c, col4c = st.columns(3)
        with col1c:
            patients, patientsID, patientsFile,patientsMap = loadPatients.getPatieents()
            # pop(0) 为标题，可以省略
            patientsID.pop(0)
            patientsIDtuple = tuple(patientsID)
            optionx = st.selectbox(
                "Patients ID",
                patientsIDtuple
            )
            listFile = patientsFile[optionx]
            patientsInfo= patientsMap[optionx]

        with col2c:
            listFiletuple = tuple(listFile)
            option = st.selectbox(
                "Slides ID",
                listFiletuple
            )


            fileImg = os.path.join(file, option)
            saveRoot = os.path.join(saveRoot, option)
            # 打开文件
            raw_image = cv.imread(fileImg, 0)
            # 预测
            segmented_img = network["function"](image=raw_image, saveRoot=saveRoot)


        # TODO 修改为过往病例查看文件树
        # TODO 病例编码
        with col4c:
            add_selectbox = st.selectbox(
                "Patients Recode(Loading)",
                patientsIDtuple
            )
        st.markdown("---")
        # TODO 改为动态页面，即时得到病例报告
        # TODO 病例报告与病人资料同步更新

    # with st.container():
    #     # TODO 展示用户各类信息

    if genre == 'Traditional':
        with st.container():
            col1, col2 = st.columns([8, 2])
            with col1:
                st.subheader("Raw and Segmentation")
            with col2:
                st.subheader("Information")

        with st.container():
            col1, col2, col3= st.columns([4, 4, 2])
            with col1:
                raw_image = cv.resize(raw_image, (800, 800), interpolation=cv.INTER_LINEAR)
                st.image(raw_image, caption="raw slides")

            with col2:
                st.image(segmented_img, caption="segmented slides")

            with col3:
                # TODO 更改为显示用户资料
                #3,4,5,6,11,17位
                #Gender\Age\Country\Diagnosis\Date\Institution

                #取得：{"Gender":inf[3],"Age":inf[4],"Country":inf[5],"Diagnosis":inf[6],"Date":inf[7],"Institution":inf[17]}
                Gender = patientsInfo["Gender"]
                Age = patientsInfo["Age"]
                Country = patientsInfo["Country"]
                Diagnosis = patientsInfo["Diagnosis"]
                Date = patientsInfo["Date"]
                Institution = patientsInfo["Institution"]
                st.write("Gender : " + Gender)
                st.write("Age : " + Age)
                st.write("Country : " + Country)
                st.write("Diagnosis : " + Diagnosis)
                st.write("Date : " + Date)
                st.write("Institution : " + Institution)
                st.markdown("---")
                # txt = st.text_area(label="Input diagnose report",height=200)





        st.markdown("---")




    if genre == 'Super View':
        with st.container():
            col1, col3, col4 = st.columns([8, 1, 1])
            with col1:
                juxtapose(raw_image,segmented_img)

            with col3:
                st.header(" ")
                raw_imageList = []
                for i in range(1, int(len(listFile) / 2)):
                    fileImg = os.path.join(file, listFile[i])
                    raw_image = cv.imread(fileImg, 0)
                    raw_image = cv.resize(raw_image, (70, 70))
                    raw_imageList.append(raw_image)
                st.image(raw_imageList)

            with col4:
                st.header(" ")
                for i in range(int(len(listFile) / 2), len(listFile)):
                    fileImg = os.path.join(file, listFile[i])
                    raw_image = cv.imread(fileImg, 0)
                    raw_image = cv.resize(raw_image, (70, 70))
                    st.image(raw_image)


    # TODO 将图像链接由静态改为动态
    # TODO 修改图像排版
    # TODO 使图像可以无极放大，大小限制在框内，突出全屏查看按钮

    with st.container():
        # st.header("Others")
        col1, col2 = st.columns([8, 2])
        with col1:
            raw_imageList = []
            if len(listFile)>6:
                values = st.slider(
                    'Select a range of slides',
                    min_value=1, max_value=len(listFile), value = 6,step=1)
                if values<6:
                    for i in range(0, int(values)):
                        fileImg = os.path.join(file, listFile[i])
                        raw_image = cv.imread(fileImg, 0)
                        raw_image = cv.resize(raw_image, (150, 150))
                        raw_imageList.append(raw_image)
                    st.image(raw_imageList, use_column_width='auto')
                else:
                    for i in range(int(values-6), int(values)):
                        if i>len(listFile)-1:
                            break
                        fileImg = os.path.join(file, listFile[i])
                        raw_image = cv.imread(fileImg, 0)
                        raw_image = cv.resize(raw_image, (150, 150))
                        raw_imageList.append(raw_image)
                    st.image(raw_imageList,use_column_width='auto')

            else:
                for i in range(0,len(listFile)):
                    fileImg = os.path.join(file, listFile[i])
                    raw_image = cv.imread(fileImg, 0)
                    raw_image = cv.resize(raw_image, (150, 150))
                    raw_imageList.append(raw_image)
                st.image(raw_imageList, use_column_width='auto')
        st.markdown("---")



    # TODO 风琴箱图

    with st.container():
        pass
        txt = st.text_area('输入病例报告')
        st.button("输入")
        st.button("清除")