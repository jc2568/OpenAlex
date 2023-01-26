import pandas as pd
import numpy as np
import time
import os,sys
import csv
import re

t0=time.time()

fileDir = "./worksAuthorship/"
aFileDir=os.path.join(fileDir)
print(aFileDir,"\n")

t0=time.time()

count=0

# Iterate directory
for path in sorted(os.listdir(aFileDir)):
    print("Processing file:",path)
    newDir=os.path.join(aFileDir,path)
    authorFile=pd.read_csv(newDir, header=None, low_memory=False, quotechar=None, quoting=3)
    authorFile.rename(columns={0:'workId',1:'authorPosition',2:'authorId'},inplace=True)

    authorFile['workId']=authorFile['workId'].str.replace('http.+?/W','',regex=True)
    authorFile['authorId']=authorFile['authorId'].str.replace('http.+?/A','',regex=True)
    authorFileFirst=authorFile.loc[authorFile['authorPosition']=='first'].copy()

    authorFileFirst.dropna(subset=['workId'],inplace=True)
    authorFileFirst.dropna(subset=['authorId'],inplace=True)
    authorFileFirst['workId']=authorFileFirst['workId'].astype('int')
    authorFileFirst['authorId']=authorFileFirst['authorId'].astype('int')

    authorFileFirst.to_csv('./worksAuthorship/worksAuthorshipReduced.csv', mode='a', index=False, header=False)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins")

os.chmod("./worksAuthorship/worksAuthorshipReduced.csv", 0o777)
