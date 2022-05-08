import os

def getPatieents():
    print(os.getcwd())
    # UPdate
    filePatient = r"..\parametersData\meta_data_covid_mini.csv"
    # Test
    # filePatient = r".\parametersData\meta_data_covid_mini.csv"
    patients = []
    patientsID = []
    patientsFile = {}
    patientsMap = {}
    with open(filePatient,"rb") as f:
        for line in f:
            inf = line.decode("cp936", 'ignore').split(",")
            patients.append(inf)
            if inf[2] in patientsID:
                patientsFile[inf[2]].append(inf[1])

            if inf[2] not in patientsID:
                patientsID.append(inf[2])
                patientsFile[inf[2]]=[inf[1]]
                # 3,4,5,6,7,17位
                # Gender\Age\Country\Diagnosis\Date\Institution
                patientsMap[inf[2]]={"Gender":inf[3],"Age":inf[4],"Country":inf[5],"Diagnosis":inf[6],"Date":inf[11],"Institution":inf[17]}

            # 记录每一个病人的信息与地址
    return patients,patientsID,patientsFile,patientsMap


if __name__ == '__main__':
    patients,patientsID,patientsFile,patientsMap = getPatieents()
