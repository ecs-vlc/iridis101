#!/bin/bash -l
#SBATCH -p ecsstudents
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH -c 32
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@soton.ac.uk
#SBATCH --time=00:4:00

module load conda/py3-latest
conda activate my-pytorch-env

python cifar.py
