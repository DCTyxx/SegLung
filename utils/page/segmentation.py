import os.path
import pandas as pd
import streamlit as st
import cv2 as cv
from ..juxtapose.Use import superView
from ..data import loadPatients
from ..data import loadRecord
from ..model.InfNet import InfNetpredict
from ..model.UNet import UNetpredict
from ..model.DeepLabV3Plus import DeeplabV3Ppredict
from ..functions.get3DSlides import buildPdbPage
from ..page.fixSegt import fixResult
import time

# have lots of things to do

def getAllSildes(listFile,file):
    raw_imageList = []
    for i in range(0, int(len(listFile))):
        fileImg = os.path.join(file, listFile[i])
        raw_image = cv.imread(fileImg, 0)
        raw_image = cv.resize(raw_image, (150, 150))
        raw_imageList.append(raw_image)
    return raw_imageList

def mainboard(job,nowFile,PatientID):
    patientsFile = r"parametersData/meta_data_covid_mini.csv"
    imageFile = r"parametersData/LungSlides"
    saveRoot = r'result/ModelResult'
    fixFile = r'result/FixResult'
    recordFile = r'UserData/userReport.csv'

    patientsFile = os.path.join(nowFile, patientsFile)
    file = os.path.join(nowFile, imageFile)
    saveRoot = os.path.join(nowFile, saveRoot)
    fixFile = os.path.join(nowFile, fixFile)
    recordFile = os.path.join(nowFile,recordFile)
    hPatientsID, hPatientsReport = loadRecord.getRecord(recordFile)


    csvframe = pd.read_csv(recordFile, names=['patientsID', 'report','Time','Doc'])


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
    placeholder1 = st.sidebar.empty()
    with placeholder1.container():

        st.markdown("## Neural Network Menu")
        network = st.selectbox(
                    "Neural Network", Network,format_func=lambda net: net["title"]
                )

        genre = st.radio(
            label="Select the view",
            options=('Super View','Traditional View'),
            index=0
        )

    # ???????????????
    with st.container():
        col1c, col2c, col4c = st.columns(3)
        with col1c:
            patients, patientsID, patientsFile,patientsMap = loadPatients.getPatieents(patientsFile)
            # pop(0) ????????????????????????
            patientsID.pop(0)
            patientsIDtuple = tuple(patientsID)
            if job==0:
                optionx = st.selectbox(
                    "Patients ID",
                    patientsIDtuple
                )
            elif job==1:
                optionx = st.selectbox(
                    "Patients ID",
                    hPatientsID
                )
            else:
                optionx = PatientID
                st.subheader("PatientID : "+optionx)


            listFile = patientsFile[optionx]
            patientsInfo= patientsMap[optionx]
            # load all the slides about this patient
            raw_imageList = getAllSildes(listFile, file)
            page = buildPdbPage(raw_imageList)


        with col2c:
            listFiletuple = tuple(listFile)
            option = st.selectbox(
                "Slides ID",
                listFiletuple
            )
            nameImage1 = option.split(".")[0]+"1.png"
            nameImage2 = option.split(".")[0]+"2.png"
            fileImg = os.path.join(file, option)
            saveRoot = os.path.join(saveRoot, option)
            fixFile = os.path.join(fixFile, option)
            # ????????????
            raw_imagex = cv.imread(fileImg, 0)
            # ??????
            segmented_img = network["function"](image=raw_imagex, saveRoot=saveRoot)
            raw_image = cv.resize(raw_imagex, (1000, 1000), interpolation=cv.INTER_LINEAR)


        # TODO ????????????????????????????????????
        # TODO ????????????
        with col4c:
            if job==0:
                result = st.checkbox("I think segmentation result is wrong", False)
                ck = False
            elif job==1:
                result = False
                ck = st.checkbox("I want to check diagnose report about this patient.", True)
            else:
                ck = False
                result = False
        # TODO ?????????????????????????????????????????????
        # TODO ???????????????????????????????????????

    # with st.container():
    #     # TODO ????????????????????????


    if result==False:
        if ck==True:
            # show the diagnose report
            # we have hPatientsID and hPatientsReport we can show information in the table
            # show the 3 record recently
            # dic = {}
            # for i in range(len(hPatientsReport[optionx])):
            #     dic[]
            #
            # st.table(data=None)
            #
            # if len(hPatientsReport[optionx]) > 3:
            #     with st.expander("See explanation"):
            #         st.table(data=None)
            pass


        if genre == 'Traditional View':
            with st.container():
                col1,col2, col3 = st.columns([5.5,2.5, 2])
                with col1:
                    st.subheader("Raw and Segmentation")
                with col2:
                    pass

                with col3:
                    st.subheader("Information")

            with st.container():
                col1, col2, col3= st.columns([4, 4, 2])
                with col1:
                    st.image(raw_image, caption="raw slides")

                with col2:
                    st.image(segmented_img, caption="segmented slides")

                with col3:
                    # TODO ????????????????????????
                    # Plot!
                    st.plotly_chart(page, use_container_width=False)

                    # TODO ???????????????????????????
                    #3,4,5,6,11,17???
                    #Gender\Age\Country\Diagnosis\Date\Institution
                    #?????????{"Gender":inf[3],"Age":inf[4],"Country":inf[5],"Diagnosis":inf[6],"Date":inf[7],"Institution":inf[17]}
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
                    # txt = st.text_area(label="Input diagnose report",height=200)
            st.markdown("---")

        if genre == 'Super View':
            with st.container():
                col1, col2, col3 = st.columns([5.5, 2.5, 2])
                with col1:
                    st.subheader("Raw and Segmentation")
                with col2:
                    pass

                with col3:
                    st.subheader("Information")


            with st.container():
                col1, col2 = st.columns([8, 2])
                with col1:
                    nameImage1 = network["title"] + nameImage1
                    nameImage2 = network["title"] + nameImage2
                    superView(raw_image,segmented_img,nameImage1,nameImage2)

                with col2:
                    # TODO ????????????????????????

                    st.plotly_chart(page, use_container_width=False)


                    # TODO ???????????????????????????
                    # 3,4,5,6,11,17???
                    # Gender\Age\Country\Diagnosis\Date\Institution
                    # ?????????{"Gender":inf[3],"Age":inf[4],"Country":inf[5],"Diagnosis":inf[6],"Date":inf[7],"Institution":inf[17]}
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

        # TODO ????????????????????????????????????
        # TODO ??????????????????
        # TODO ??????????????????????????????????????????????????????????????????????????????

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
        # TODO ????????????
        if job == 0:
            with st.container():
                placeholder2 = st.empty()
                with placeholder2:
                    txt = st.text_area('Enter your report',placeholder="Please input diagnose report about this patient.")
                if st.button("Submit"):
                    # record]
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                    frame = pd.DataFrame([[optionx, txt,t,PatientID]],columns=['patientsID', 'report','Time','Doc'])
                    frame.to_csv(recordFile, mode='a', header=False,index=False )

        elif job == 1:
            st.subheader("diagnose report")

            flag = 1
            for i in range(len(csvframe)):
                if str(csvframe['patientsID'][i]) == optionx:
                    flag=0
                    st.write(str(csvframe['report'][i]))

            if flag==1:
                st.write("The doctor did not give a diagnosis report, you can push your diagnosis.")

            if flag==1 or st.checkbox("I think segmentation result is wrong", False):
                txt = st.text_area('Enter your report', placeholder="Please input diagnose report about this patient.")
                if st.button("Submit"):
                    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    frame = pd.DataFrame([[optionx, txt,t,PatientID]],columns=['patientsID', 'report','Time','Doc'])
                    frame.to_csv(recordFile, mode='a', header=False,index=False)

        else:
            st.subheader("diagnose report")
            flag = 1
            for i in range(len(csvframe)):
                if str(csvframe['patientsID'][i]) == optionx:
                    flag=0
                    st.write(str(csvframe['report'][i]))

            if flag==1:
                st.write("The doctor did not give a diagnosis report.")


    else:
        placeholder1.empty()
        fixResult(raw_imagex,segmented_img,fixFile)
