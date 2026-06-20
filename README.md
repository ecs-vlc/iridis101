# Training CIFAR-10 on IRIDIS and SWARM

Iridis is the University's supercomputer. Currently on the 6th generation, Iridis 6 houses over 50,000 cores of HPC, coupled with a state of the art storage backend. Iridis X is the name of the part of the service that contains GPU accelerators; it is disinct from Iridis 6 compute, but uses the same storage backbone. Iridis X is also the template for the upcoming Iridis 7 which is currently (2026) being procured. Iridis X contains a number of partitions/nodes with different GPUs: Nvidia L4s, L40s, A100s, H100s and H200s and a node based around the AMD MI200. 

IridisX includes SWARM (the Southampton Wolfson Ai Research Machine), a £700K investment in 10x compute nodes for use by research staff in ECS and the Optoelectronics Research Centre. This investment includes: 5x Compute nodes each with 4x 80GB A100 SXM GPU nodes, 2x Compute nodes each with 8x 80GB H100 SXM GPU nodes, and 3x nodes with 7x 24GB L4 GPUs, giving users access to the very latest technology from Nvidia. In addition ECS has been investing in the next generation of student-facing compute with new nodes based around a 7x L4 24GB GPUs per node architecture for teaching use, which is also accessed through Iridis X, and utlitises the same storage platform.

The systems run batch jobs using the SLURM job scheduler and utilise features such as quality of service (QOS) and partition scavenging. Applications typically run using the standard machine learning framework, Python, Tensorflow, PyTorch, Keras, all of which are supported and maintained centrally.

## Running jobs on Iridis X / SWARM / ecsstudents

ECS Staff and PhD students have access to SWARM nodes automatically. ECS students need to request access to the ecsstudents nodes by registering [here](https://sotonproduction.service-now.com/serviceportal?id=kb_article_view&sysparm_article=KB0083316).

Iridis X is accessed via the iridis 5 login nodes using SSH:

	ssh loginx001.iridis.soton.ac.uk

or alternatively via `iridisX002` or `iridisX003`.

The first time you log in to the login node you need to create a python environment and install any dependencies to run your code. This environment will be available on the compute nodes when your jobs run. We'll create an environment and setup pytorch and torchbearer:

	module load conda/py3-latest
	conda create -n "my-pytorch-env" python=3.13
	conda activate my-pytorch-env
	pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu132
	pip install packaging torchbearer

When we login in the future we can just activate the environment:

	module load conda/py3-latest
	conda activate my-pytorch-env

Lets also clone this git repository so we can try training a model:

	git clone https://github.com/ecs-vlc/iridis101.git
	cd iridis101

The repository contains three files: this readme, a python script for training ResNet18 models on CIFAR-10 ("cifar.py"), and a SLURM Batch script ("launch.sh") which is configured to run the python script on SWARM. Before launching the job we need to be aware that the Iridis compute nodes do not have direct internet access, and so cannot download files. Before running the script, we first need to download the data; the script is capable of doing this for us by just running it on the login node:

	python cifar.py

This will run until an error occurs when pytorch tries to access the GPU (the not all the login nodes have GPUs), but by that point the data will have already been downloaded. If your login node does have a GPU then `ctrl-c` to stop the process once the data has been downloaded.

Next edit the SLURM script in an editor like vim, and change the email address to match your own. You'll see that the SLURM script contains a number of lines starting with `#SBATCH` which are instructions to tell SLURM what computational resources you need (one GPU on one node on the `ecsstudents' partition, 32GB of RAM, 6 CPU cores) and how long you want to run the code for (defaults to 4 minutes in this script). Everything else just enables your conda python environment and runs the code. 

To launch a job we just run:

	sbatch launch.sh

You'll get email status updates when the job starts and finishes. From the login node you'll see a log file is created in the directory you ran `sbatch` and eventually see the trained model file once it gets created. You can watch the log file get filled up with:

	tail slurm-<slurm_job_id>.log

using the job id printed by sbatch when you ran it.

**Other useful things:**

- `squeue` lets you look at the queue
- `scancel` lets you cancel a queued/running job based on the job id
- when a job is running you can ssh into the node (look at squeue to see which node) and run `top` and `nvidia-smi` to monitor resource usage
- `nvidia-smi -dmon` is really useful for monitoring throughput

