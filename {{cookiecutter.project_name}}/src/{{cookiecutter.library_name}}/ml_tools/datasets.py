"""Definition of the project's pytorch datasets.

File defining the pytorch datasets used for training in this case.
"""
import logging
import os
from collections import OrderedDict
from typing import Any, List

import numpy as np
import torch
from sqlalchemy.sql import text
from {{cookiecutter.library_name}}.utils.sql import load_session
from torch.utils.data import Dataset

logger = logging.getLogger("ml_tools.datasets")


# We iterate through this list of keys to ensure the ordering stays consistent.
# This might be superfluous
ORDERED_VARIABLES = ["y", "state"]


class {{ cookiecutter.class_prefix }}Dataset(Dataset):
    """Custom wrapper on torch's Dataset class."""

    def __init__(
        self,
        static_values: dict[str, Any],
        dataset_path: str,
    ) -> None:
        """Initialize the dataset class.

        Parameter
        -------
        static_values: dict
            Statistical properties related to an entire dataset.
            These are passed into the normalize_data function

        dataset_path : str
            path to a directory containing .pt files

        """
        self.dataset_path = dataset_path
        self.static_values = static_values

        all_files = []
        for element in os.listdir(dataset_path):
            if "dataset_statistics" in element:
                continue
            all_files.append(element)
        self.snippets = sorted(all_files)

    def __len__(self):
        """Return how many snippet file that exist."""
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

        # Normalize data
        normalized_data = normalize_data(data, static_values=self.static_values)
        normalized_data = torch.Tensor(np.array(list(normalized_data.values())))
        out = normalized_data.flatten()
        return out


###############################################################
# Data extraction and preprocessing


def retrieve_data_from_sql(sql_table: str, start_date: str, end_date: str) -> Any:
    """Function that extracts raw data from postgres.

    In addition to the variables extracted from postgres, This function also creates
    separate variables for time components such as the second, minute, hour and day of
    the week.

    Feel free to add / remove these depending on the resolution and periodicity of your
    time series.
    """
    session = load_session()

    statement = text(
        f"""SELECT
                time,
                y
            FROM
                {sql_table}
            WHERE
                time BETWEEN '{start_date}' AND '{end_date}'
            ORDER BY 1;
        """
    )

    returned = session.execute(statement)
    data: OrderedDict[str, Any] = OrderedDict()

    data["month"] = []
    data["day"] = []
    data["weekday"] = []
    data["hour"] = []
    data["minute"] = []
    for i, x in enumerate(returned):
        row = dict(x._mapping)
        for k, v in row.items():
            if i == 0:
                data[k] = []
            data[k].append(v)

            if k == "time":
                data["month"].append(v.month)
                data["day"].append(v.day)
                data["weekday"].append(v.weekday())
                data["hour"].append(v.hour)
                data["minute"].append(v.minute)

    return data


def gather_dataset_statistics(df: dict[Any, Any]) -> dict[Any, Any]:
    """Compute statistical properties of individual dataset.

    This function looks at all dataset variables, and saves some of their properties in
    static_values, which can later be used alongside the normalizing function.
    """
    static_values: dict[str, Any] = {}

    for k, v in df.items():
        if k == "time":
            continue
        v = [e if e is not None else 0.0 for e in v]
        v = np.array(v, dtype=float)
        static_values[k] = {
            "mean": np.nanmean(v),
            "std": np.nanstd(v, ddof=1),
            "min": np.nanmin(v),
            "max": np.nanmax(v),
            "median": np.nanmedian(v),
        }

    return static_values


def produce_snippets(
    df: dict, time_window: int, include_keys: list = ORDERED_VARIABLES
) -> Any:
    """Take a historical dataset and cut it into snippets of specified dimensions.

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

    Returns:
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


def normalize_data(df: dict[Any, Any], static_values: dict[Any, Any]) -> dict[Any, Any]:
    """Normalize data, if needed with static values.

    Use this function to apply simple
    transformation to your data like
    normalizing values between -1 and 1

    Parameters:
    ---

    df : dict
        Raw dataset extracted from retrieve_from_sql

    static_values: dict
        dictionary of precalculated normalization values,
        usually based on the training dataset
    """
    for k, v in df.items():
        if k == "time":
            continue

        # Clear None's and convert to NaN
        v = [e if e is not None else 0.0 for e in v]
        v = np.array(v, dtype=float)

        if k == "some_large_variable":
            v = np.log10(v + 1)

        mu = static_values[k]["mean"]
        sigma = static_values[k]["std"]
        df[k] = (v - mu) / sigma

    return df


#########################
