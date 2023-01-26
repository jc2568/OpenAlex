import pandas as pd
import numpy as np
import time
import os,sys
import csv

"""
Author: Joshua Chu
Data: October 28, 2022

This Python script was written to merge author name and publication position with the work id
that corresponds to the publication. There are several records that do not have author id
corresponding to the work id, but downstream work identified these records are only missing the
author id and most, if not all, of the remaining data is present. In other words, the only piece
of data missing was the author name. In most cases, this renders the record useless when using
this data for the RoS dataset, but these records will be maintained anyway in case other analyses
can utilize the data.

Command structure: python3 aaWorkIdAuthorIdMerge.py

"""

t0=time.time()

### contains the authors Ids and author names. The data type for the author id was explicitly
### assigned to ensure the data types for both datasets are the same
df1=pd.read_csv("./authors/authorsReducedFinal.tsv",sep='\t', header=None, low_memory=False)
df1.rename(columns={0:'authorId',1:'authorName'},inplace=True)

print("authorsReducedFilteredMod.tsv was imported and columns renamed\n",flush=True)

df1['authorId']=df1['authorId'].astype(int)

print("Strings were processed in the authorId column and changed to int dtype\n",flush=True)
df1.info(null_counts=True)


### contains the works Ids, author position in paper, and author Ids
df2=pd.read_csv("./worksAuthorship/worksAuthorshipReduced.csv", header=None, low_memory=False)
df2.rename(columns={0:'workId',1:'authorPosition',2:'authorId'},inplace=True)

print("The worksAuthorshipReduced.csv file was imported and columns renamed\n",flush=True)
df2.info(null_counts=True)


### merge the authorsReducedFinal.csv and worksAuthorshipReduced.csv using the authorId field.
### An outer merge was performed to maintain records that did not contain author names. Further,
### the overall size of the resulting output was reduced to create a smaller dataset
df1Outerdf2=df1.merge(df2,on=['authorId'],how='outer',indicator=True)
df1Mergedf2=pd.concat([df1Outerdf2.loc[df1Outerdf2['_merge']=='both'],df1Outerdf2.loc[df1Outerdf2['_merge']=='right_only']],axis=0)
df1Mergedf2Sub=df1Mergedf2.iloc[:,0:4]

print("The authorsReduced.csv and worksAuthorshipReduced.csv files were merged\n",flush=True)
df1Mergedf2Sub.info(null_counts=True)


### save the file and change the permissions for all to have access
df1Mergedf2Sub.to_csv("./worksIdAuthorsIdNameMerge.csv",index=False)
print("The merged was successful and saved as worksIdAuthorsIdNameMerge.csv\n",flush=True)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins\n")

df1Mergedf2Sub.info(null_counts=True)

os.chmod("./worksIdAuthorsIdNameMerge.csv", 0o777)
