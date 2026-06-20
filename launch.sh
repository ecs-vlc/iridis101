#!/bin/bash -l
#SBATCH -p l4,scavenger_l4,slurm_a100
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH -c 6
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@soton.ac.uk
#SBATCH --time=00:4:00

module load conda/python3
conda activate my-pytorch-env

python cifar.py
