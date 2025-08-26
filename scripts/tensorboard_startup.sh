#!/bin/bash

# Set environment variable (can help in some environments)
export XDG_RUNTIME_DIR=""

# Random port
tb_port=$(shuf -i8000-9999 -n1)

# Get node and user info
node=$(hostname -s)
user=$(whoami)

logdir="logs"

# Echo SSH tunnel info
echo -e "
Tensorboard:
ssh -N -L ${tb_port}:${node}:${tb_port} ${user}@login.rci.cvut.cz
http://localhost:${tb_port}
"

# Load Jupyter + Python module from /mnt
ml IPython/8.28.0-GCCcore-13.3.0

cd ..

PYTHON_PATH=$(which python3)
echo "Using Python interpreter: ${PYTHON_PATH}"

if [ ! -d "./venv" ]; then
    ${PYTHON_PATH} -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install notebook
    pip install ipykernel
    pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple \
            cddlt
    python -m ipykernel install --user --name=venv --display-name "Python (venv)"
fi

source venv/bin/activate

cd scripts/

# Start TensorBoard
tensorboard --logdir=${logdir} --port=${tb_port} --bind_all &

# ./train_all.sh
