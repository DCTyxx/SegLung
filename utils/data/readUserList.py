import pandas as pd

def read(file,name):
    csvframe = pd.read_csv(file,names=["name","password"])
    for i in range(len(csvframe)):
        if str(csvframe['name'][i]) == name:

            """
            TODO: 返回UID对应的password
            """
            return str(csvframe['password'][i])


if __name__ == '__main__':
    file = "../userList.csv"
    pwd = read(file,'xxy')