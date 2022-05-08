import pandas as pd

def record(name,password,file):
    frame = pd.DataFrame([[name,password]],
                         columns=['name','password'])
    frame.to_csv(file, mode='a',index=False, header=False,)

# if __name__ == '__main__':

    # record(name='jyl',password='123456',file=file)