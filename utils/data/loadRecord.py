import pandas as pd

def getRecord(recordFile):
    # record all patients ID,just like [patient1,patient2,patient3......]
    patientsID = []
    # record all patients report dic,just like {ID:[{doc1:{time1:report1}},{doc1:{time2:report2}},{doc1:{time3:report3}}......]}
    patientsReport={}

    csvframe = pd.read_csv(recordFile, names=['patientsID', 'report','Time','Doc'])
    for i in range(len(csvframe)):
        pId = str(csvframe['patientsID'][i])
        if pId not in patientsID:
            patientsID.append(pId)
            patientsReport[pId] = [{csvframe['Doc'][i]: {csvframe['Time'][i]:csvframe['report'][i]}}]
        else:
            patientsReport[pId].append({csvframe['Doc'][i]: {csvframe['Time'][i]: csvframe['report'][i]}})

    return patientsID,patientsReport