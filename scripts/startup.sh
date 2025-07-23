#!/bin/bash

# Set environment variable (can help in some environments)
export XDG_RUNTIME_DIR=""

# Random port
port=$(shuf -i8000-9999 -n1)

# Get node and user info
node=$(hostname -s)
user=$(whoami)

# Echo SSH tunnel info
echo -e "
MacOS or Linux terminal command to create your ssh tunnel:
ssh -N -L ${port}:${node}:${port} ${user}@login.rci.cvut.cz

MobaXterm info:

Forwarded port: same as remote port
Remote server: ${node}
Remote port: ${port}
SSH server: login.rci.cvut.cz
SSH login: ${user}
SSH port: 22

Use a Browser on your local machine to go to:
http://localhost:${port}
"

# move to downscale directory
cd ..

# Load Jupyter + Python module from /mnt
ml IPython/8.28.0-GCCcore-13.3.0

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

# Start Jupyter Notebook
jupyter notebook --no-browser --port=${port} --ip=0.0.0.0
