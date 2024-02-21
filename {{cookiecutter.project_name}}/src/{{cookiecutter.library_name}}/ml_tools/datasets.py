""" File defining the different variants of 
pytorch datasets used for training in this case.

"""
import os
from typing import Any

import numpy as np
import torch
from torch.utils.data import Dataset


class {{ cookiecutter.class_prefix }}Dataset(Dataset):
    def __init__(
        self,
        model_params: dict[str, Any],
        dataset_path: str,
    ) -> None:
        """Initialize the dataset class.

        Parameter
        -------
        model_type: str
            defines how the data is split

        dataset_path : str
            path to a directory containing .pt files

        """
        self.dataset_path = dataset_path
        self.model_params = model_params

        all_files = []
        for element in os.listdir(dataset_path):
            all_files.append(element)
        self.snippets = sorted(all_files)

    def __len__(self):
        return len(self.snippets)

    def __getitem__(self, idx):
        """Define the way we load data into the DataLoader.
        This example simply loads pre-saved torch tensor
        files
        """
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # The snippet tensor dimension should have size
        data = torch.load(os.path.join(self.dataset_path, self.snippets[idx]))

        out = data.flatten()

        return out


#########################
def normalize_data(df: dict[Any, Any]) -> dict[Any, Any]:
    """Placeholder function

    Use this function to apply simple 
    transformation to your data like 
    normalizing values between -1 and 1
    """
    pass

#########################