#!/bin/bash

#SBATCH --job-name="sub_second"
#SBATCH --partition=rtx3090
#SBATCH --propagate=NONE
#SBATCH -vvv
#SBATCH --ntasks=4
#SBATCH --mem=32G
#SBATCH --time=0-00:01:00
#SBATCH --output=slurm-outputs/gpu_info.out
#SBATCH -q hca-csd765
#SBATCH --gpus 3
#SBATCH -A ddp325

echo "$(nvidia-smi)"