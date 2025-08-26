import torch
import argparse
import torchmetrics

from typing import Tuple, Optional

def args_setup(
    args: argparse.Namespace,
    model: torch.nn.Module
) -> Tuple[torch.optim.Optimizer, Optional[torch.optim.lr_scheduler.CosineAnnealingLR], torch.nn.modules.loss._Loss]:

    opt = args.optimizer.strip().lower()
    if opt == "adam":
        optimizer = torch.optim.Adam(params=model.parameters(), lr=args.lr, weight_decay=args.wd)
    elif opt == "adamw":
        optimizer = torch.optim.AdamW(params=model.parameters(), lr=args.lr, weight_decay=args.wd)
    else:
        raise ValueError(f"Unsupported optimizer: {args.optimizer}")

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs) \
        if args.scheduler else None

    loss_type = args.loss.strip().upper()
    if loss_type == "MSE":
        loss = torch.nn.MSELoss()
    elif loss_type == "L1":
        loss = torch.nn.L1Loss()
    else:
        raise ValueError(f"Unsupported loss: {args.loss}")
    
    return optimizer, scheduler, loss
