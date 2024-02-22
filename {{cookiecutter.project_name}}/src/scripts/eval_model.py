"""Script to run an evaluation of the trained models"""
import glob
import logging
import os
from pathlib import Path
from typing import Any

import hydra
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
import torch
from {{cookiecutter.library_name}}.ml_tools.datasets import (
    retrieve_data_from_sql,
    {{cookiecutter.class_prefix}}Dataset,
    produce_snippets
    )
from {{cookiecutter.library_name}}.ml_tools.models import {{cookiecutter.class_prefix}}AE, {{cookiecutter.class_prefix}}ARIMA, {{cookiecutter.class_prefix}}LSTM
from omegaconf import DictConfig

project_path = Path(__file__).parents[2]

logger = logging.getLogger("train_model")
logger.level = logging.INFO


class ModelEvaluator:
    """Evaluation class for a model."""

    def __init__(
        self,
        model,
        model_type: str,
        state_dict_path: str | None = None,
    ) -> None:
        """Provide the trained model information.

        Parameters:
        ---

        model : torch.nn.Module
            architecture of the model trained

        model_type: str
            The type of model we are evaluating

        state_dict_path : str
            path to the ".pt" file storing the trained weights
            of the model
        """
        self.model = model
        if state_dict_path is not None:
            self.model.load_state_dict(torch.load(state_dict_path))
        self.model.eval()
        self.model_type = model_type

    def evaluate(self, dataset):
        """decide which evaluation to perform based on the model type."""

        if self.model_type == "output_predictor":
            data = self._prediction_accuracy(dataset=dataset)
        else:
            print("NOTHING PLANED FOR ANOMALY ENCODER")
        return data

    def plot_anomaly_latent_space(self, training_set, test_set):
        """
        We plot the Latent space visualization of the training
        and test dataset, using the PCA decomposition function
        fitted to the train data.

        The goal of this plot is to confirm that the test data
        maps out the same regions of the latent space as the
        training data

        """
        fig, ax = plt.subplots(figsize=(10, 10))

        train_samples = []
        for i, d in enumerate(training_set):
            d = torch.unsqueeze(d, dim=0)
            latent_representation = self.model.encoder(d)
            array = latent_representation.cpu().detach().numpy()
            train_samples.append(array.flatten())

        train_samples = np.array(train_samples)
        pca = PCA(n_components=2)
        pca_model = pca.fit(train_samples)
        reduced_values_train = pca_model.transform(train_samples)

        # plot the training set first
        ax.scatter(
            reduced_values_train[:, 0],
            reduced_values_train[:, 1],
            label="training data",
            alpha=0.3,
        )

        test_samples = []
        for i, d in enumerate(test_set):
            d = torch.unsqueeze(d, dim=0)
            latent_representation = self.model.encoder(d)
            array = latent_representation.cpu().detach().numpy()
            test_samples.append(array.flatten())

        test_samples = np.array(test_samples)
        pca = PCA(n_components=2)
        reduced_values_test = pca_model.transform(test_samples)
        ax.scatter(
            reduced_values_test[:, 0],
            reduced_values_test[:, 1],
            label="test data",
            alpha=0.3,
        )
        ax.legend()
        plt.show()

    def plot_prediction_accuracy(self, data, labels: dict[Any, Any] | None = None):
        """compare the reconstructed time series with the original data."""

        n_channels = data["real"].shape[0]
        fig, axes = plt.subplots(
            n_channels, figsize=(10, 20 * n_channels), gridspec_kw={"hspace": 1.0}
        )
        fig.suptitle("Output Predictor - Accuracy")

        for i in range(n_channels):
            if n_channels == 1:
                ax = axes
            else:
                ax = axes[i]

            if labels is None:
                label = f"output {i}"
            else:
                label = labels[i]

            ax.set_title(label)
            ax.plot(data["real"][i, :], label="real data")
            ax.plot(data["pred"][i, :], label="prediction")

            handles, lbs = ax.get_legend_handles_labels()
        fig.legend(handles, lbs, loc="center right")
        plt.show()

    def _prediction_accuracy(self, dataset):
        """Evaluate the accuracy of the model's prediction,for a given dataset."""
        self.model.cpu()

        real = []
        pred = []
        for y in dataset:
            all_inputs, outputs = y

            # add batch dimension to inputs
            all_inputs = torch.unsqueeze(all_inputs.cpu(), 0)

            # restore dimensionality of output
            outputs = torch.reshape(
                outputs, (self.model.predict_dims, self.model.predict_window)
            )

            prediction = self.model(all_inputs)
            prediction = torch.reshape(
                prediction, (self.model.predict_dims, self.model.predict_window)
            )

            pred.append(prediction.detach().numpy())
            real.append(outputs.detach().numpy())

        pred = np.hstack(pred)
        real = np.hstack(real)

        difference = (pred - real) / (real) * 100.0

        n_under = sum(difference < 0.0)
        n_over = len(difference) - n_under

        total_under = sum(difference[difference < 0.0])
        avg_under = np.median(difference[difference < 0.0])
        std_under = np.std(difference[difference < 0.0])

        total_over = sum(difference[difference > 0.0])
        return {
            "n_under": n_under,
            "n_over": n_over,
            "total_over": total_over,
            "total_under": total_under,
            "median_under_prediction": avg_under,
            "sigma_under_prediction": std_under,
            "real": real,
            "pred": pred,
            "diff": difference,
        }


@hydra.main(version_base=None, config_path="../../config", config_name="config")
def main(config: DictConfig) -> None:
    """Run evalutation code for several trained models."""
    
    for training_conf in config["ml_trainings"]:
        model_type = list(training_conf.keys())[0]
        training_conf = training_conf[model_type]
        training_name = training_conf["name"]
        model_params = training_conf["model"]["model_params"]

        # Get training data
        train_data = {{cookiecutter.class_prefix}}Dataset(
            model_type=model_type,
            model_params=model_params,
            dataset_path=f"./{training_name}_train_dataset/",
        )

        if (
            model_type == "output_predictor"
            and training_conf["model"]["name"] == "{{cookiecutter.class_prefix}}LSTM"
        ):
            logger.info("Evaluating an LSTM model...")
            evaluator = ModelEvaluator(
                model={{cookiecutter.class_prefix}}LSTM(**model_params),
                model_type=model_type,
                state_dict_path=f"./{training_name}.pt",
            )

            # Plot the accuracy of the prediction
            data = evaluator.evaluate(dataset=train_data)

            param_labels = model_params["predict_variables"]
            evaluator.plot_prediction_accuracy(data=data, labels=param_labels)

        elif (
            model_type == "output_predictor"
            and training_conf["model"]["name"] == "DynflexARIMA"
        ):
            logger.info("Evaluating an ARIMA model...")
            evaluator = ModelEvaluator(
                model={{cookiecutter.class_prefix}}ARIMA(**model_params),
                model_type=model_type,
            )

            # Plot the accuracy of the prediction
            data = evaluator.evaluate(dataset=train_data)

            param_labels = model_params["predict_variables"]
            evaluator.plot_prediction_accuracy(data=data, labels=param_labels)

        elif model_type == "anomaly_encoder":
            evaluator = ModelEvaluator(
                model={{cookiecutter.class_prefix}}AE(**model_params),
                model_type=model_type,
                state_dict_path=f"./{training_name}.pt",
            )

            # create a test dataset
            dataset_path = f"./{training_name}_test_dataset/"
            if not os.path.isdir(dataset_path):
                os.makedirs(dataset_path)

            if len(glob.glob(dataset_path + "/*.pt")) == 0:
                dataset_info = config["datasets"][1].dataset
                time_periods = dataset_info["time_periods"]
                df = retrieve_data_from_sql(
                    start_date=time_periods["start"],
                    end_date=time_periods["end"],
                )

                current, past = produce_snippets(
                    df=df, time_window=model_params["input_window"]
                )
                for n, (c, p) in enumerate(zip(current, past)):
                    torch.save(
                        (c, p), dataset_path + f"/{model_type}_test_sample_{n:0>6d}.pt"
                    )

            test_dataset = {{cookiecutter.class_prefix}}Dataset(
                model_type=model_type,
                model_params=model_params,
                dataset_path=dataset_path,
            )
            evaluator.plot_anomaly_latent_space(
                training_set=train_data, test_set=test_dataset
            )


if __name__ == "__main__":
    main()
