#!/bin/bash -l
#SBATCH -p ecsstudents
#SBATCH --mem=32G
#SBATCH --gres=gpu:0
#SBATCH --nodes=1
#SBATCH -c 32
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your_email@soton.ac.uk
#SBATCH --time=00:4:00

module load conda/py3-latest
#conda activate torchbearer
export NCCL_DEBUG=INFO
export PYTHONFAULTHANDLER=1

python hw.py
