import pandas as pd
import numpy as np
import time
import os,sys
import csv
import re

"""
Author: Joshua Chu
Data: October 28, 2022

The Python script was written to prepare the works.csv data for merging with the
worksIdVenueIdBiblioAuthorIdNameMerge.csv dataset. The works.csv file is too large
to be directly merged and was split by utilizing the chuncksize metric in the
read_csv function. Processing steps were introduced in the script below to format
the data and ensure the subsequent merge step would not experience problems. The
subsetted files were saved and permissions changed for all to have access.

Command structure: python3 aaProcessSplitWorksFiles.py

"""

t0=time.time()

### this imports data AND creates the subfiles by utilizing the chunksize
### metric. The processing steps includes extracting the work Id, removing
### new lines and tabs from the title, extra spaces in strings, changing
### the field names, and converting years and dates to integers
df = pd.read_csv("./works.csv", low_memory=False, chunksize=5000000)
a=0
for data in df:
    data.dropna(subset=['publication_year'],inplace=True)
    data.iloc[:,0]=data.iloc[:,0].str.replace('^.+?W','')
    data.title=data.title.replace("\n","",regex=True)
    data.title=data.title.replace("\t"," ",regex=True)
    data.title=data.title.replace("  "," ",regex=True)
    data1=data.iloc[:,[0,2,4]].copy()
    data1.rename(columns={'id':'workId','publication_year':'year'},inplace=True)
    data1.title=data1.title.replace("  "," ",regex=True)
    data1.year=data1.year.astype(int)
    data1.workId=data1.workId.astype(int)
    filename='works.'+str(a)
    filepath=os.path.join("./works",filename)
    data1.to_csv(filepath,index=False)
    os.chmod(filepath,0o777)
    a=a+1

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins\n", flush=True)

data1.info(null_counts=True)
