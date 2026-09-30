#!/bin/bash -l
#SBATCH -p ecsstudents_l4
#SBATCH -A ecsstudents
#SBATCH --mem=1G
#SBATCH --nodes=1
#SBATCH -c 1
#SBATCH --time=00:00:10

echo "$HOSTNAME says Hello World"
