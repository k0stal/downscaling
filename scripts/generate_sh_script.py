import os
import argparse

from itertools import product
from typing import List, Dict, Union, Any

parser = argparse.ArgumentParser()
parser.add_argument("--split", default=False, type=bool)

### Hyperparameter grid

hyperparams: Dict[str, Dict[str, List[Union[float, str, bool]]]] = {
    #"bicubic": {
    #    "loss": ["MSE", "L1"],
    #    "epochs": 35
    #},
    
    #"srcnn": {
    #   "lr": [1e-4],
    #   "wd": [1e-5],
    #   "optimizer": ["Adam"],
    #   "scheduler": True,
    #   "epochs": 200,
    #   "loss": ["L1"]
    #},
    
    #"espcn": {
    #    "lr": [1e-3, 1e-5],
    #    "wd": [0, 1e-5],
    #    "optimizer": ["Adam"],
    #    "scheduler": True,
    #    "epochs": 35,
    #    "loss": ["MSE", "L1"]
    #},

    "edsr": {
       "lr": [1e-4],
       "wd": [1e-5],
       "optimizer": ["Adam"],
       "scheduler": True,
       "epochs": 300,
       "loss": ["L1"],
       "blocks_nr": [64],
       "features": [128],
    },

    "swinir": {
        "lr": [1e-4],
        "wd": [1e-5],
        "optimizer": ["AdamW"],
        "scheduler": True,
        "epochs": 300,
        "loss": ["L1"], #MSE
        "rstb": [6],
        "stl": [6],
        "window_size": [8],
        "att_head_nr": 6
    },

    "fno": {
         "lr": [1e-3],
         "wd": [0],
         "optimizer": ["Adam"],
         "scheduler": True,
         "epochs": 500,
         #"loss": ["MSE", "L1"],
         "loss": ["MSE"],
         "layers": [7],
         "hidden_size": [64],
         "freq_cutoff": [14]
    },

    # "deepesdtas": {
    #     "lr": [1e-4],
    #     "wd": [0, 1e-5],
    #     "optimzier": ["Adam", "AdamW"],
    #     "scheduler": True,
    #     "epochs": 35,
    #     "loss": ["L1", "MSE"],
    #     "filters_last_conv": [8, 16, 32]
    # }
}

def generate_commands(model: str, params: Dict[str, List[Any]]) -> List[str]:
    commands = []
    param_names = list(params.keys())
    param_values = [params[name] for name in param_names]
    param_values = [param if type(param) == list else [param] for param in param_values]
    
    for values in product(*param_values):
        command = f"python3 {model}.py"
        for name, value in zip(param_names, values):
            if isinstance(value, bool):
                command += f" --{name}={str(value).lower()}"
            else:
                command += f" --{name}={value}"
        commands.append(command)
    
    return commands

def main(args: argparse.Namespace) -> None:
    if args.split:
        for model, params in hyperparams.items():
            commands = generate_commands(model, params)
            with open(f"{model}.sh", "w") as f:
                for command in commands:
                    f.write(command + "\n")
    else:
        all_commands = []
        for model, params in hyperparams.items():
            commands = generate_commands(model, params)
            all_commands.extend(commands)
        
        with open("train_all.sh", "w") as f:
            for command in all_commands:
                f.write(command + "\n")

if __name__ == "__main__":
    main_args = parser.parse_args([] if "__file__" not in globals() else None)
    main(main_args)
