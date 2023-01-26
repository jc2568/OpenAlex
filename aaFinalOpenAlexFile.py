import pandas as pd
import numpy as np
import time
import os,sys
import csv

"""
Author: Joshua Chu
Data: October 28, 2022

The Python script was written to merge the subsetted works.csv files individually with the
bibliography/author/journal data using the work id as the key for the inner merge. The file
variable is set to use a system argument, which allows this script to easily be parallelized.
The output files are saved with a merge suffix and saved in the ./OpenAlexMerges directory
and will be concatenated using one final script.

Command structure: python3 aaFinalOpenAlexFile.py

"""

t0=time.time()

### the file variable takes a system argument; this script is specifically setup for parallelizing
### subfiles in the ./works directory with the worksIdVenueIdBiblioAuthorIdNameMerge.csv file. The
### script can be used to individually process the subfiles in ./works or you can use the slurm
### code. See documentation for details
file = sys.argv[1]
print("Processing file:",file[8:],"\n",flush=True)


### imports data and selects specific columns to be utilized in the merge
bibAuthJournal=pd.read_csv("./worksIdVenueIdBiblioAuthorIdNameMerge.csv",usecols=['workId','volume','issue','firstPage','lastPage','journal','authorName'],low_memory=False)
print("The worksIdVenueIdBiblioAuthorIdNameMerge.csv file has been imported for merging","\n",flush=True)
bibAuthJournal.info(null_counts=True)


### imports the subfile to be merged with the above data; drops any records that does
### not contain a year and converts the year and work id to integer data type
workSubs=pd.read_csv(file,low_memory=False)
#workSubs1=workSubs[pd.to_numeric(workSubs['workId'],errors='coerce').notnull()].reset_index(drop=True).copy()
#workSubs1.workId=workSubs1.workId.astype(np.int64)

workSubs1=workSubs.dropna(subset=['year']).copy()
workSubs1.year=workSubs1.year.astype(int)
workSubs1.workId=workSubs1.workId.astype(int)

print("File",file[8:],"has been imported and dtypes verified","\n",flush=True)

workSubs1.info(null_counts=True)


### performs an inner merge using the work id as the key
workSubsMerge=workSubs1.merge(bibAuthJournal,on=['workId'],how='inner').iloc[:,[2,0,3,4,5,6,8,1,7]]


### creates the file name and saves the data; permissions are changed to provide
### access to all users
filename=file[8:]+'.merge'+'.tsv'
filepath=os.path.join('./openAlexMerges',filename)

workSubsMerge.to_csv(filepath,sep="\t", header=None, index=False)
#workSubs1.to_csv(filepath,sep="\t", header=None, index=False)
print("The files have been merged and saved as openalex.tsv\n",flush=True)

t1=time.time()
total=t1-t0
print("Total time is %4f" % (total/60), "mins\n", flush=True)

workSubsMerge.info(null_counts=True)
#workSubs1.info(null_counts=True)

os.chmod(filepath, 0o777)
