""" File defining the different variants of 
pytorch datasets used for training in this case.
"""
import os
import logging
from typing import Any

import numpy as np
import torch
from sqlalchemy.sql import text
from torch.utils.data import Dataset
from {{cookiecutter.library_name}}.utils.sql import load_session

logger = logging.getLogger("ml_tools.datasets")

# We iterate through this list of keys to
# ensure the ordering stays consistent.
# this might be superfluous
ORDERED_VARIABLES = ["y", "state"]

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
def retrieve_data_from_sql(start_date: str, end_date: str) -> Any:
    """Function that extracts raw data from postgres"""
    session = load_session()

    statement = text(
        f"""SELECT
                time,
                y
            FROM
                clean_example_data
            WHERE 
                time BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY 1;
        """
    )

    returned = session.execute(statement)
    data: OrderedDict[str, Any] = OrderedDict()

    for i, x in enumerate(returned):
        row = dict(x._mapping)
        for k, v in row.items():
            if i == 0:
                data[k] = []
            data[k].append(v)
    return data



def produce_snippets(
    df: dict, time_window: int, include_keys: list = ORDERED_VARIABLES
) -> Any:
    """This function takes a historical dataset, and cuts it into
    snippets of specified dimensions

    The snippets can be taken defined as past or future observation,
    depending on the sign of the time_window variable. In both cases,
    the "current" time point is included in the array

    Parameters
    ----
    df : dict
        dictionary of time series data

    time_window: int
        number of time steps to keep. negative means past values

    include_keys: list
                    a list of keys we want to include in the
                    snippet

    Returns
    ---

    snippets : list
        a list of produced snippets of data

    current_pt : list
        a list of the values defined as the "current" value
        associated with the snippet
    """
    n_data_points = len(df[list(df.keys())[0]])

    i = 0
    current_pts: List[Any] = []
    snippets: List[Any] = []
    while i < n_data_points:
        if time_window < 0 and i < (-time_window):
            logger.debug(f"{i}: lower than time window {time_window}")
            i += 1
            continue

        if time_window >= 0 and i > (n_data_points - time_window):
            logger.debug(
                f"{i}: higher than n_datapoints - time window \
                {n_data_points-time_window}"
            )
            break

        current_pt: dict[Any, Any] = {}
        snippet: dict[Any, Any] = {}

        for k in include_keys:
            v = df[k]
            if time_window < 0:
                subv = v[(i + time_window) : i]
            else:
                subv = v[i + 1 : (i + 1 + time_window)]

            current_pt[k] = [v[i]]
            snippet[k] = subv

        if len(snippet[list(snippet.keys())[0]]) == 0:
            break
        snippets.append(snippet)
        current_pts.append(current_pt)
        i += 1

    return current_pts, snippets


def normalize_data(df: dict[Any, Any]) -> dict[Any, Any]:
    """Placeholder function

    Use this function to apply simple 
    transformation to your data like 
    normalizing values between -1 and 1
    """
    return df

#########################
