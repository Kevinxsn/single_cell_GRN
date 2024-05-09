set -eo pipefail
cd ../data
# Download chromatin accessibility reads in bam format
wget -q -o /dev/null -O bams.bam https://s3-us-west-2.amazonaws.com/10x.files/samples/cell-arc/2.0.0/pbmc_granulocyte_sorted_10k/pbmc_granulocyte_sorted_10k_atac_possorted_bam.bam
# Split bam file to individual bam files for each cell using helper script `split_bam.sh`
dictys_helper split_bam.sh bams.bam bams --section "CB:Z:" --ref_expression expression.tsv.gz
rm bams.bam