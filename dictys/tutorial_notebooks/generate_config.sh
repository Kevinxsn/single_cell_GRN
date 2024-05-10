#!/bin/bash

#SBATCH --job-name="config"
#SBATCH --partition=rtx3090
#SBATCH --propagate=NONE
#SBATCH -vvv
#SBATCH --ntasks=4
#SBATCH --mem=64G
#SBATCH --time=0-24:00:00
#SBATCH --output=slurm-outputs/slurm-main.out
#SBATCH -q hca-csd765
#SBATCH --gpus 3
#SBATCH -A ddp325

rm -Rf ../makefiles
mkdir ../makefiles
cd ../makefiles

echo "Starting job at $(date)"

dictys_helper makefile_template.sh common.mk config.mk env_none.mk static.mk
dictys_helper makefile_update.py ../makefiles/config.mk '{"DEVICE": "cuda:0", "GENOME_MACS2": "hs", "JOINT": "1"}'
cd .. && dictys_helper makefile_check.py

# Network inference
dictys_helper network_inference.sh -j 32 -J 1 static 
echo "Finished job at $(date)"