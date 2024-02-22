"""Script for training a model on the example IOTML data."""

import glob
import logging
import os
from typing import Any

import hydra
import matplotlib.pyplot as plt
import numpy as np

import torch
from {{cookiecutter.library_name}}.ml_tools.datasets import (
    {{cookiecutter.class_prefix}}Dataset,
    normalize_data,
    produce_snippets,
    retrieve_data_from_sql
    )
from {{cookiecutter.library_name}}.ml_tools.models import {{cookiecutter.class_prefix}}AE, {{cookiecutter.class_prefix}}Loss, {{cookiecutter.class_prefix}}LSTM
from {{cookiecutter.library_name}}.ml_tools.traintest import {{cookiecutter.class_prefix}}TrainTest
from omegaconf import DictConfig
from sklearn.decomposition import PCA

logger = logging.getLogger("train_model")
logger.level = logging.INFO


def train_model(
    model_type: str,
    output_name: str,
    dataset_path: str,
    model_params: dict[Any, Any] = {},
    training_params: dict[Any, Any] = {},
) -> Any:
    """Training script for a single model."""

    logger.info("training model...")

    if model_type == "anomaly_encoder":
        model_instance = {{cookiecutter.class_prefix}}AE(**model_params)
        loss_instance = {{cookiecutter.class_prefix}}Loss()
    elif model_type == "output_predictor":
        model_instance = {{cookiecutter.class_prefix}}LSTM(**model_params)
        loss_instance = {{cookiecutter.class_prefix}}Loss()
    else:
        raise Exception("Unrecognized model type.")

    traintest = {{cookiecutter.class_prefix}}TrainTest(
        model=model_instance,
        model_type=model_type,
        optimizer=torch.optim.Adam(
            model_instance.parameters(), lr=training_params["learning_rate"]
        ),
        loss_fn=loss_instance,
        device="cuda",
    )

    # add the train and valid dataset to the algo
    train_data = {{cookiecutter.class_prefix}}Dataset(
        model_type=model_type,
        model_params=model_params,
        dataset_path=dataset_path,
    )
    traintest.add_dataset("train", train_data, batch_size=training_params["batch_size"])
    traintest.current_dataset = "train"
    traintest.train(
        dataset_label="train", n_epochs=training_params["n_epochs"], autosave=False
    )
    traintest.save_trained_model(output_name=output_name)

    return traintest.loss_history


def return_pca_inputs(model, dataset):
    """Compute the PCA projection of the data using the latent space of model."""

    train_samples = []
    for i, d in enumerate(dataset):
        # the model is expecting a batch vector,
        # so we need to add an extra dimension at the beginning
        d = torch.unsqueeze(d, dim=0)
        latent_representation = model.encoder(d.to("cuda"))
        array = latent_representation.cpu().detach().numpy()
        train_samples.append(array.flatten())

    all_samples = np.array(train_samples)
    return all_samples


def define_pca_space(model, train_data):
    """Fit the PCA function to a particular dataset and model."""

    all_samples = return_pca_inputs(model=model, dataset=train_data)

    #
    # Determine the PCA of the training sample in latent space
    #
    pca = PCA(n_components=2)
    pca_model = pca.fit(all_samples)
    return pca_model


######################################################################
# Plotting functions
#
def plot_latent_space_pca(ds_name: str, reduced_values: np.ndarray):
    """Plot2D projection of the PCA components using matplotlib."""
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_ylim([-2, 6])
    ax.set_xlim([-5, 6])
    # plot the training set first
    ax.scatter(
        reduced_values[:, 0], reduced_values[:, 1], label=f"{ds_name} data", alpha=0.3
    )
    ax.legend()
    plt.show()


######################################################################
@hydra.main(version_base=None, config_path="../../config", config_name="config")
def main(config: DictConfig) -> None:
    """main orchestrating function.

    given some datasets, run the training and
    evaluations that are appropriate to run
    """
    # parse config file for the datasets we need
    dataset = config["datasets"][0].dataset
    dataset_name = dataset["name"]
    time_periods = dataset["time_periods"]
    logger.info("step 1 - Creating a training dataset...")
    logger.info("Load data from postgres..")
    df = retrieve_data_from_sql(
        start_date=time_periods["start"],
        end_date=time_periods["end"],
    )
    logger.info("normalizing / handling NaN values")
    df_norm = normalize_data(df.copy())

    if logger.level == logging.DEBUG:
        logger.debug("Plotting variables before / after normalization...")

        for k, v in df.items():
            v = [e if e is not None else 0.0 for e in v]
            v = np.array(v)
            fig, axes = plt.subplots(2, 2, figsize=(14, 7))
            axes[0, 0].plot(v, label="variable")
            axes[0, 0].set_title(f"variable: {k}")
            axes[1, 0].hist(v[v != 0], bins=35)
            axes[1, 0].set_title("variable distribution")
            axes[0, 0].legend()

            v_normed = df_norm[k]
            axes[0, 1].plot(v_normed, label="variable", color="g")
            axes[0, 1].set_title(f"variable: {k}- NORMALIZED")
            axes[1, 1].hist(v_normed[v_normed != 0.0], bins=35, color="g")
            axes[1, 1].set_title("normalized distribution")
            axes[0, 1].legend()
            plt.show()

    for train_conf in config["ml_trainings"]:
        # shortcut for the training dict hierarchy
        model_type = dir(train_conf)[0]
        train_conf = train_conf.get(model_type)

        # information about the model
        model_params = train_conf["model"]["model_params"]
        if train_conf["model"]["name"] == "{{cookiecutter.class_prefix}}ARIMA":
            logger.info("Detected an ARIMA model. These do not need to be trained")
            continue

        # information about the training
        training_name = train_conf["name"]
        training_params = train_conf["training_params"]
        dataset_path = f"./{training_name}_{dataset_name}_dataset/"
        logger.info(f"\n\n---- training model: {training_name} ---\n\n")

        if not os.path.isdir(dataset_path):
            logger.info(f"no dataset path, creating it ({dataset_path})")
            os.makedirs(dataset_path)

        if len(glob.glob(dataset_path + "/*.pt")) == 0:
            logger.info(
                f"Path {dataset_path} is empty. generating time series snippets..."
            )
            _, past = produce_snippets(
                df=df,
                time_window=model_params["input_window"],
                include_keys=model_params["input_variables"].values(),
            )
            current, _ = produce_snippets(
                df=df,
                time_window=model_params["input_window"],
                include_keys=model_params["predict_variables"].values(),
            )

            for n, (c, p) in enumerate(zip(current, past)):
                torch.save(
                    (c, p),
                    dataset_path
                    + f"/{training_name}_{dataset_name}_sample_{n:0>6d}.pt",
                )
                n_dims = len(list(p.keys()))
                n_time = len(p[list(p.keys())[0]])
            logger.info(
                f"Done. generated {n} snippets of {n_dims} dims x {n_time} time windows"
            )
        else:
            logger.info("Dataset already created.")

        logger.info('Step 2: Train a model on the "train" dataset...')
        if not os.path.isfile(training_name + ".pt"):
            # Run the training
            output = train_model(
                model_type=model_type,
                dataset_path=dataset_path,
                output_name=training_name + ".pt",
                model_params=model_params,
                training_params=training_params,
            )

            plt.plot(output, "k")
            plt.title(f"Loss over iterations - {model_type}")
            plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("Train a model on example data")
    datasets = {  # Training phase: start periods with only a few days of opened park
        "train": {"start": "2024-01-01 00:00:00", "end": "2024-01-01 15:00:00"},
    }
    main()
