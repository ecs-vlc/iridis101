#!/bin/bash -l
#SBATCH -p ecsstudents_l4
#SBATCH -A ecsstudents
#SBATCH --mem=24G
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH -c 6
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@soton.ac.uk
#SBATCH --time=00:4:00

module load conda/python3
conda activate my-pytorch-env

python cifar.py
