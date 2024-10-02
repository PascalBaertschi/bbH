#!/bin/bash
# 
#SBATCH --partition=standard
#SBATCH --account=t3
#SBATCH --time=11:00:00
#SBATCH --mem-per-cpu=5G
#SBATCH -o logfiles/slurm_%A_%a.log
#SBATCH --get-user-env



echo job start at 
date
echo SLURM_JOB_ID: $SLURM_JOB_ID
echo HOSTNAME: $HOSTNAME
echo JOBLIST:$1
mkdir -p /scratch/$USER/${SLURM_JOB_ID}
echo Going to execute
echo $(cat $1 | sed -n ${SLURM_ARRAY_TASK_ID}p)
eval $(cat $1 | sed -n ${SLURM_ARRAY_TASK_ID}p)
rmdir  /scratch/$USER/${SLURM_JOB_ID}


echo Complete at 
date
