#!/bin/bash
#SBATCH --partition=gpulong
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --mem=128g
#SBATCH --job-name=downscaling
#SBATCH --output=./slurm_logs/downscaling-%j-%a.log
#SBATCH --array=0-0

mkdir -p ./slurm_logs/

ml IPython/8.28.0-GCCcore-13.3.0

cd ..

echo "Using Python interpreter: $(which python3)"

# Activate pre-created virtual environment
if [ -d "./venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found."
    exit 1
fi

cd scripts/

cmd=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" train_all.sh)
echo "Running command: $cmd"

srun $cmd
