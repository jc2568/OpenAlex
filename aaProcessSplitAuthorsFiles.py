import pandas as pd
import numpy as np
import time
import os,sys
import csv
import re

t0=time.time()

fileDir = "./authors/"
aFileDir=os.path.join(fileDir)
print(aFileDir,"\n")

t0=time.time()

count=0

# Iterate directory
for path in sorted(os.listdir(aFileDir)):
    print("Processing file:",path)
    newDir=os.path.join(aFileDir,path)
    authorFile=pd.read_csv(newDir, header=None, low_memory=False, quotechar=None, quoting=3)
    authorFile=authorFile[~authorFile[0].str.contains('"')]
    authorFile=authorFile[~authorFile[0].str.contains("'")]
    authorFile[0]=authorFile[0].str.replace('http.+?/A','',regex=True)
    authorFile.dropna(subset=[0],inplace=True)
    authorFile.dropna(subset=[1],inplace=True)
    authorFile=authorFile[~authorFile[0].str.contains("[A-z]")]
    authorFile[0]=authorFile[0].astype('int')

    authorFile.to_csv('./authors/authorsReduced.csv', mode='a', index=False, header=False)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins")

os.chmod("./authors/authorsReduced.csv", 0o777)
