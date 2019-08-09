#!/bin/bash
#$ -V
#$ -j yes
#$ -q normal-e3
#$ -pe distrib 16
#$ -cwd
#$ -m bea
#$ -M fine.wilms@deltares.nl

cd $SGE_O_WORKDIR
 

~/anaconda3/bin/python ~/Overtopping_for_copy/scripts/compare_models.py 

