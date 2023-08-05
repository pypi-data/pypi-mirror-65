#!/bin/bash

# Copyright 2020 by Peter Cock, The James Hutton Institute.
# All rights reserved.
# This file is part of the THAPBI Phytophthora ITS1 Classifier Tool (PICT),
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

IFS=$'\n\t'
set -eu
# Note not using "set -o pipefail" until after check error message with grep

export TMP=${TMP:-/tmp}

echo "Preparing sample data for recycled water example"

mkdir -p tests/recycled_water/raw_data/
cd tests/recycled_water/raw_data/
if [ ! -f "SRR6303948_1.fastq.gz" ]; then
    curl ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR630/008/SRR6303948/SRR6303948_1.fastq.gz
fi
if [ ! -f "SRR6303948_2.fastq.gz" ]; then
    curl ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR630/008/SRR6303948/SRR6303948_2.fastq.gz
fi
cd ../../..

rm -rf $TMP/recycled_water
mkdir $TMP/recycled_water
mkdir $TMP/recycled_water/raw_data
mkdir $TMP/recycled_water/intermediate_default
mkdir $TMP/recycled_water/intermediate_primers

ln -s tests/recycled_water/raw_data/SRR6303948_1.fastq.gz $TMP/recycled_water/raw_data/
ln -s tests/recycled_water/raw_data/SRR6303948_2.fastq.gz $TMP/recycled_water/raw_data/

echo "======================"
echo "Checking prepare-reads"
echo "======================"
set -x

# Default primers
thapbi_pict prepare-reads -i $TMP/recycled_water/raw_data/ -o $TMP/recycled_water/intermediate_default

diff $TMP/recycled_water/intermediate_default/SRR6303948.fasta tests/recycled_water/intermediate_default/SRR6303948.fasta

# Actual primers
thapbi_pict prepare-reads -i $TMP/recycled_water/raw_data/ -o $TMP/recycled_water/intermediate_primers \
 --left GAAGGTGAAGTCGTAACAAGG --right AGCGTTCTTCATCGATGTGC
diff $TMP/recycled_water/intermediate_primers/SRR6303948.fasta tests/recycled_water/intermediate_primers/SRR6303948.fasta

echo "$0 - test_receycled_water.sh passed"
