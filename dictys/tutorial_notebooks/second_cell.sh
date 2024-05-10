#!/bin/bash

#SBATCH --job-name="sub_second"
#SBATCH --partition=rtx3090
#SBATCH --propagate=NONE
#SBATCH -vvv
#SBATCH --ntasks=4
#SBATCH --mem=64G
#SBATCH --time=0-23:00:00
#SBATCH --output=slurm-outputs/slurm-main.out
#SBATCH -q hca-csd765
#SBATCH --gpus 1
#SBATCH -A ddp325


set -eo pipefail
cd ../data
echo "current_file $(pwd)"
# Download chromatin accessibility reads in bam format
echo "start job at $(date)"
echo "Begin Downloading files"
wget -q -o /dev/null -O bams.bam https://s3-us-west-2.amazonaws.com/10x.files/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_atac_possorted_bam.bam
echo "finish downloading"
# Split bam file to individual bam files for each cell using helper script `split_bam.sh`
dictys_helper split_bam.sh bams.bam bams --section "CB:Z:" --ref_expression expression.tsv.gz
rm bams.bam
echo "end job at $(date)"