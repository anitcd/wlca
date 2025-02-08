#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N WLCA_PCAg
#$ -cwd
#$ -l h_rt=47:59:59
#$ -l h_vmem=16G
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 5 minutes: -l h_rt
#  memory limit of 1 Gbyte: -l h_vmem
# Initialise the environment modules
. /etc/profile.d/modules.sh
module load anaconda
source activate AIMCISC_o1

# Load Python
#module load python/3.4.3

# Run the program
sh test_wlca.sh $1 $2 $3 $4 $5

