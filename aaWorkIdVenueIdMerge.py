import pandas as pd
import numpy as np
import time
import os,sys
import csv

"""
Author: Joshua Chu
Data: October 28, 2022

This Python script is designed to merge two datasets: venues.csv and works_host_venues.csv files. Both
files contain a venue key that will be utilized to merge the datasets. But before the merge can be
performed, the http:// address must be processed. For the venues.csv file, only the venue id is needed
to be prepared, while the venue id and work id must be processed in the works_host_venues.csv file. After
the data prep is finished, an inner merge is performed and the resulting dataset is saved with the
permissions changed for all to access.

Command structure: python3 aaWorkIdVenueIdMerge.py

"""

t0=time.time()

### the venues.csv file contains the venues and venues Id. The file must be processed prior to merging
### and the resulting venue ids will be sorted and the field names will be standardized to merge with
### subsequent data
df1=pd.read_csv("./venues.csv",usecols=['id','display_name'])
df1.rename(columns={'id':'venueId','display_name':'journal'},inplace=True)

print("Venues.csv was imported and columns renamed\n",flush=True)
df1.info(null_counts=True)

df1['venueId']=df1['venueId'].str.replace('http.+?/V','',regex=True)
df1.sort_values(by=['venueId'],ascending=True,inplace=True)
df1=df1.reset_index(drop=True)

print("The Venue Id was processed and sorted in ascending order\n",flush=True)
df1.info(null_counts=True)


### the works_host_venues.csv file contains work Id and venues Id that must be processed prior to
### merging with the venues.csv data. The field names will be standardized to merge with subsequent
### data
df2=pd.read_csv("./works_host_venues.csv",usecols=['work_id','venue_id'])
df2.rename(columns={'work_id':'workId','venue_id':'venueId'},inplace=True)

print("The works_host_veneus.csv file was imported and columns renamed\n",flush=True)
df2.info(null_counts=True)

df2['workId']=df2['workId'].str.replace('http.+?/W','',regex=True)
df2['venueId']=df2['venueId'].str.replace('http.+?/V','',regex=True)
df2=df2.reset_index(drop=True)

print("The workId and venueId was processed\n",flush=True)
df2.info(null_counts=True)


### the two datasets were merged using an inner merge and applying the venueId as the key. The stats
### for the resulting merge will be printed to confirm the merge happened as expected
df1Mergedf2=df1.merge(df2,on=['venueId'],how='inner')

print("The venues.csv file and primary file were merged\n",flush=True)
df1Mergedf2.info(null_counts=True)


### save data and change the permissions for all to access
df1Mergedf2.to_csv("./worksIdVenueIdMerge.csv",index=False)
print("The merged files were saved as worksIdVenueIdMerge.csv\n",flush=True)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins\n")

df1Mergedf2.info(null_counts=True)

os.chmod("./worksIdVenueIdMerge.csv", 0o777)
