import pandas as pd
import numpy as np
import time
import os,sys
import csv

"""
Author: Joshua Chu
Data: October 28, 2022

This Python script was written to merge the bibliography data and the author data from
previously constructed datasets. The work id is the key used to perform the outer merge
and join the two sets. An outer merge was performed because some of the records did not
have bibliography data, but most of the other data was present. Therefore, data without
these data were preserved and included in the final dataset

Command structure: python3 aaWorkIdVenueIdBiblioAuthorIdNameMerge.py

"""

t0=time.time()

### contains the bibliography data and journal name for all works
df1=pd.read_csv("./worksIdVenueIdBiblioMerge.csv",low_memory=False)

print("The worksIdVenueIdBiblioMerge.csv was imported\n",flush=True)
df1.info(null_counts=True)


### contains the work id, author name, and author position within the publication
df2=pd.read_csv("./worksIdAuthorsIdNameMerge.csv",low_memory=False)

print("The worksIdAuthorsIdNameMerge.csv file was imported and ready to merge with the bibliography data\n",flush=True)
df2.info(null_counts=True)


### perform an outer merge between the datasets using the work id is the key. An outer
### merge was performed to preserve work ids that may not have a complete bibliography
### record
df1Outerdf2=df1.merge(df2,on=['workId'],how='outer',indicator=True)
df1Mergedf2=pd.concat([df1Outerdf2.loc[df1Outerdf2['_merge']=='both'],df1Outerdf2.loc[df1Outerdf2['_merge']=='left_only']],axis=0)
df1Mergedf2Sub=df1Mergedf2.iloc[:,:10].reset_index(drop=True)
df1Mergedf2Sub.drop_duplicates(keep='first', inplace=True)

print("The merge was successful\n",flush=True)

### saves the data and changes the permissions
df1Mergedf2Sub.info(null_counts=True)
df1Mergedf2Sub.to_csv("./worksIdVenueIdBiblioAuthorIdNameMerge.csv",index=False)

print("The merge was saved as worksIdVenueIdBiblioAuthorIdNameMerge.csv\n",flush=True)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins\n")

df1Mergedf2Sub.info(null_counts=True)

os.chmod("./worksIdVenueIdBiblioAuthorIdNameMerge.csv", 0o777)
