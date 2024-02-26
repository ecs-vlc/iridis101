# Training CIFAR-10 on IRIDIS, Lyceum and ECS Alpha

Iridis is the University's supercomputer. Currently on the 5th generation, Iridis 5 contains a range of accelerators ranging from GTX1080 machines through V100 multi accelerator nodes to Dual A100 nodes. Lyceum is a partition of Iridis 5
available for taught student use. In 2020 Iridis 5 was expanded with the ECS Alpha partition, a £200K investment for the School of Electronics and Computer Science (ECS) in 6x compute nodes each with 4x 48GB Nvidia GPU cards available for the schools’ research staff and students.

The scheduled launch of the latest iteration Iridis 6 in the coming months will house over 50,000 cores of HPC. This will include SWARM (the Southampton Wolfson Ai Research Machine), £700K investment in 7x compute nodes for use by research staff in ECS and the Optoelectronics Research Centre. This investment includes: 5x Compute nodes each with 4x 80GB A100 SXM GPU nodes and 2x Compute nodes each with 8x 80GB H100 SXM GPU nodes, giving users access to the very latest technology from Nvidia.

The systems run batch jobs using the SLURM job scheduler and utilise features such as quality of service (QOS) and partition scavenging. Applications typically run using the standard machine learning framework, Python, Tensorflow, PyTorch, Keras, all of which are supported and maintained centrally.

## Running jobs on Alpha

Staff and students have access to Alpha automatically. Alpha is accessed via the iridis 5 login nodes using SSH:

	ssh iridis5_a.soton.ac.uk

or alternatively via `iridis5_b` or `iridis5_c`.

The first time you log in to the login node you need to create a python environment and install any dependencies to run your code. This environment will be available on the compute nodes when your jobs run. We'll create an environment and setup pytorch and torchbearer:

	module load conda/py3-latest
	conda create -n "my-pytorch-env" python=3.10
	conda activate my-pytorch-env
	conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
	pip install packaging torchbearer

When we login in the future we can just activate the environment:

	module load conda/py3-latest
	conda activate my-pytorch-env

Lets also clone this git repository so we can try training a model:

	git clone https://github.com/ecs-vlc/iridis101.git
	cd iridis101

The repository contains three files: this readme, a python script for training ResNet18 models on CIFAR-10 ("cifar.py"), and a SLURM Batch script ("launch.sh") which is configured to run the python script on Alpha. Before launching the job we need to be aware that the Iridis compute nodes (and Alpha) do not have direct internet access, and so cannot download files. Before running the script, we first need to download the data; the script is capable of doing this for us by just running it on the login node:

	python cifar.py

This will run until an error occurs when pytorch tries to access the GPU (the login node doesn't have one!), but by that point the data will have already been downloaded.

Next edit the SLURM script in an editor like vim, and change the email address to match your own. You'll see that the SLURM script contains a number of lines starting with `#SBATCH` which are instructions to tell SLURM what computational resources you need (one GPU on one node on the Alpha "ecsstudents" partition], 32GB of RAM, 32 CPU cores) and how long you want to run the code for (defaults to 4 minutes in this script). Everything else just enables your conda python environment and runs the code. 

To launch a job we just run:

	sbatch launch.sh

You'll get email status updates when the job starts and finishes. From the login node you'll see a log file is created in the directory you ran `sbatch` and eventually see the trained model file once it gets created. You can watch the log file get filled up with:

	tail slurm-<slurm_job_id>.log

using the job id printed by sbatch when you ran it.

Other useful things:

	- `squeue` lets you look at the queue
	- `scancel` lets you cancel a queued/running job based on the job id
	- when a job is running you can ssh into the node (look at squeue to see which node) and run `top` and `nvidia-smi` to monitor resource usage
	- `nvidia-smi -dmon` is really useful for monitoring throughput

