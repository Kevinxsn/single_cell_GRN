#!/bin/bash

#SBATCH --job-name="config"
#SBATCH --partition=rtx3090
#SBATCH --propagate=NONE
#SBATCH -vvv
#SBATCH --ntasks=4
#SBATCH --mem=64G
#SBATCH --time=0-24:00:00
#SBATCH --output=slurm-outputs/slurm-test.out
#SBATCH -q hca-csd765
#SBATCH --gpus 3
#SBATCH -A ddp325


cd ../data
wget -q -o /dev/null https://cf.10xgenomics.com/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_analysis.tar.gz
#Extract cell names for each cluster
tar xf pbmc_granulocyte_sorted_10k_analysis.tar.gz 
mv analysis/clustering/gex/graphclust/clusters.csv clusters.csv
rm -Rf pbmc_granulocyte_sorted_10k_analysis.tar.gz analysis

subsets="$(tail -n +2 clusters.csv | awk -F , '{print $2}' | sort -u)"
echo "$subsets" | awk '{print "Subset"$1}' > subsets.txt
for x in $subsets; do
	mkdir -p "subsets/Subset$x"
	grep ",$x"'$' clusters.csv | awk -F , '{print $1}' > "subsets/Subset$x/names_rna.txt"
	# RNA and ATAC barcodes are the same for joint quantifications
	cp "subsets/Subset$x/names_rna.txt" "subsets/Subset$x/names_atac.txt"
done
rm clusters.csv



wget -q -o /dev/null -O motifs.motif 'https://hocomoco11.autosome.org/final_bundle/hocomoco11/full/HUMAN/mono/HOCOMOCOv11_full_HUMAN_mono_homer_format_0.0001.motif'
dictys_helper genome_homer.sh hg38 genome
wget -q -o /dev/null -O gene.gtf.gz http://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/Homo_sapiens.GRCh38.107.gtf.gz
gunzip gene.gtf.gz
dictys_helper gene_gtf.sh gene.gtf gene.bed
rm gene.gtf

rm -Rf filtered_feature_bc_matrix


rm -Rf ../makefiles
mkdir ../makefiles
cd ../makefiles
dictys_helper makefile_template.sh common.mk config.mk env_none.mk static.mk
dictys_helper makefile_update.py ../makefiles/config.mk '{"DEVICE": "cpu", "GENOME_MACS2": "hs", "JOINT": "1"}'


cd .. && dictys_helper makefile_check.py
dictys_helper network_inference.sh -j 32 -J 1 static 