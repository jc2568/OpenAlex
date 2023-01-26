#!/bin/bash

TEMPFILE=./slurmfile.slurm
echo "merging worksIdVenueIdMerge.csv and bibliography information"
echo "#!/bin/bash" > $TEMPFILE
echo "#SBATCH -p large" >> $TEMPFILE
echo "#SBATCH -J CreateOA" >> $TEMPFILE
echo "#SBATCH -t 14-00:00" >> $TEMPFILE
echo "#SBATCH -n 32" >> $TEMPFILE
echo "#SBATCH --wckey=marxnfs1" >> $TEMPFILE
echo "" >> $TEMPFILE
echo "python3 aaWorkIdVenueIdBiblioMerge.py" >> $TEMPFILE
sbatch $TEMPFILE
sleep 0.1
