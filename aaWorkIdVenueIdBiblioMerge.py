import pandas as pd
import numpy as np
import time
import os,sys
import csv

"""
Author: Joshua Chu
Data: October 28, 2022

This Python script is designed to add bibiography data to the previously constructed worksIdVenueIdMerge.csv
file. The works_biblio.csv file contains the biblio data and will utilize the work id as the key to perform
an inner merge. Like before the http:// address must be processed in the works_biblio.csv file prior to
merging the data. Following a successfull merge, the file will be saved with the permissions changed for all
to access.

Command structure: python3 aaWorkIdVenueIdBiblioMerge.py

"""

t0=time.time()

### contains bibliography information for all works. The field names must be modified and the work id processed
### to facilitate the merge with the worksIdVenueIdBiblioMerge.csv file. The raw data was 'dirty' and the
### work ids needed to be converted to an integer data type in order for the merge to work
df1=pd.read_csv("./works_biblio.csv")
df1.rename(columns={'work_id':'workId','first_page':'firstPage','last_page':'lastPage'},inplace=True)

print("The bibliography data was imported and columns renamed\n",flush=True)
df1.info(null_counts=True)

df1['workId']=df1['workId'].str.replace('http.+?/W','',regex=True)
df1['workId']=df1['workId'].astype(int)
df1=df1.reset_index(drop=True)

print("The bibliography data was processed\n",flush=True)
df1.info(null_counts=True)


### contains the data with venue id, venue name, and work id
df2=pd.read_csv("./worksIdVenueIdMerge.csv")

print("The worksIdVenueIdMerge.csv file was imported and ready to merge with the bibliography data\n",flush=True)
df2.info(null_counts=True)


### perform the merge between the bibliography data and venue data. An outer merge was performed to account
### for records that did not have a work or venue id attached to them (yes the raw data contained records with no
### ids attached). In subsequet steps, it was determined this was not needed and the records that contained
### no ids were dropped anyway. The code was not modified because this had no negative impact. If desired,
### the code can be changed but it is not needed.
df1Outerf2=df1.merge(df2,on=['workId'],how='outer',indicator=True)
df1Mergedf2=pd.concat([df1Outerf2.loc[df1Outerf2['_merge']=='left_only'],df1Outerf2.loc[df1Outerf2['_merge']=='both']],axis=0).iloc[:,:7]


### the resulting merge was saved and permissions were changed
df1Mergedf2.info(null_counts=True)
df1Mergedf2.to_csv("./worksIdVenueIdBiblioMerge.csv",index=False)

print("The merge was successful and saved as worksIdVenueIdBiblioMerge.csv\n",flush=True)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins\n")

df1Mergedf2.info(null_counts=True)

os.chmod("./worksIdVenueIdBiblioMerge.csv", 0o777)
