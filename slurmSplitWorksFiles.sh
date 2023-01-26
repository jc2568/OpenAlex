#!/bin/bash

split -d --verbose -l5000000 worksSub.csv ./works/works.

FILES="./works/works.*"

for i in $FILES
do

 TEMPFILE=./slurmfile.slurm
 echo "doing $i"
 echo "#!/bin/bash" > $TEMPFILE
 echo "#SBATCH -p large" >> $TEMPFILE
 echo "#SBATCH -J CreateOA" >> $TEMPFILE
 echo "#SBATCH -t 14-00:00" >> $TEMPFILE
 echo "#SBATCH --wckey=marxnfs1" >> $TEMPFILE
 echo "#SBATCH -n 32" >> $TEMPFILE
 echo "" >> $TEMPFILE
 echo "sed -e '1s/.*/id,doi,title,display_name,publication_year,publication_date,type,cited_by_count,is_retracted,is_paratext,cited_by_api_url,abstract_inverted_index/' $i" >> $TEMPFILE
sbatch $TEMPFILE
sleep 0.1
done
