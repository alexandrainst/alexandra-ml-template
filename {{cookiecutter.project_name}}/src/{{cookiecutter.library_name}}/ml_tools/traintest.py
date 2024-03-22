"""File containing the training and testing classes.

They classes are used to schedule and coordinate an ML training phase.
"""

import logging

import numpy as np
import torch
from sklearn.decomposition import PCA
from torch.utils.data import DataLoader

logger = logging.getLogger("ml_tools.traintest")


# Generic Train Test class. avoid changing this as much as possible
class AlgoTraining:
    """Wrapper class around training steps of a pytorch model."""

    def __init__(self, model, optimizer, loss_fn, device):
        """Initialize the training class."""
        self.model = model.to(device)
        self.loss = loss_fn
        self.optim = optimizer
        self.device = device
        self.datasets = {}
        self.current_dataset = None

        # In debug mode, fix the random seed
        if logger.level == logging.DEBUG:
            logger.debug(
                "Running in debug mode. Avoiding randomness as much as possible..."
            )
            torch.manual_seed(0)

            # Also avoid using non-deterministic algorithms when running, e.g.,
            # convolutions:
            torch.use_deterministic_algorithms(True)

        # Record historic evolution of the training
        self._setup_training_logs()

    def _setup_training_logs(self):
        """Setup structure of training results and specific variables to track."""
        self.loss_history = []

    def add_dataset(self, label, dataset, batch_size=10):
        """Import new pytorch datasets and load them as DataLoders."""
        self.datasets[label] = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        self.current_dataset = label

    def _train_one_epoch(self):
        """Most important function: defines a single training step."""
        for databatch in self.datasets[self.current_dataset]:
            # get data onto computing device
            data = databatch.to(self.device)

            # reset optimizer
            self.optim.zero_grad()

            # Reconstruct tensor
            predictions = self.model(data)

            # Compute the Loss
            loss = self.loss(data, predictions)
            self.loss_history.append(loss.item())
            loss.backward()

            # run a step of optimization
            self.optim.step()

    def train(self, dataset_label="train", n_epochs=10, autosave=True):
        """Function that calls the training step over a particular dataloader."""
        self.current_dataset = dataset_label
        self.loss_history = []

        for i in range(n_epochs):
            if (i + 1) % 10 == 0:
                print(f"Epoch: {i}")
                print("-------------------------")
            self._train_one_epoch()

        print("DONE. I am done training.")
        if autosave:
            self.save_trained_model()

    def record_session(self, output_prefix: str | None = None):
        """Save model + training metadata to file."""
        if output_prefix is None:
            model_name = type(self.model).__name__
            loss_name = type(self.loss).__name__
            optim_name = type(self.optim).__name__
            output_prefix = f"{model_name}_{loss_name}_{optim_name}_\
            trained_on_{self.current_dataset}"

        self.save_trained_model(output_name=output_prefix + ".pt")
        self.save_training_metadata(output_name=output_prefix + "_metadata.pt")

    def save_trained_model(self, output_name: str) -> None:
        """Save the trained model to .pt format."""
        torch.save(self.model.state_dict(), output_name)
        logger.info(f"Saved model to {output_name}.")

    def save_training_metadata(self, output_name: str) -> None:
        """Save the training metadata (fx. the loss function history)."""
        metadata = {"loss_history": self.loss_history}
        torch.save(metadata, output_name)
        logger.info(f"Saved model metadata to {output_name}.")


#####################################################
# Project specific class. This is where you can adapt
# the training algorithm to your needs


class {{cookiecutter.class_prefix}}Training(AlgoTraining):
    """In case a project requires customize training.

    If the particular project needs more custom training style, it
    is recommended to create a seaparate project-specific test-train
    class that inherits the basics of the AlgoTrainTest class.

    One can therefter substitute basic functions with custom ones, such as
    train_one_epoch in this case.
    """

    def __init__(self, model, model_type, optimizer, loss_fn, device="cuda"):
        """Initialize inherited class + extra parameters."""
        AlgoTraining.__init__(
            self, model=model, optimizer=optimizer, loss_fn=loss_fn, device=device
        )
        self.model_type = model_type

        # Example where we want to record PCA fits of an encoder model
        self.pca_fit = None
        self.pca_data = []

    def _train_one_epoch(self):
        """Override of the generic training.

        We override the generic training
        because we need to distinguish the process
        for the two types of models we train.
        """
        for databatch in self.datasets[self.current_dataset]:
            # Reset optimizer
            self.optim.zero_grad()

            # This is where the change happens
            if self.model_type == "output_predictor":
                # get data onto computing device
                inputs, outputs = databatch
                inputs = inputs.to(self.device)
                target = outputs.to(self.device)
                predictions = self.model(inputs)

            else:
                inputs = databatch.to(self.device)
                predictions = self.model(inputs)
                target = inputs

            # Compare the predicted and target values
            loss = self.loss(target, predictions)
            self.loss_history.append(loss.item())
            loss.backward()

            # Run a step of optimization
            self.optim.step()

    def fit_pca_to_dataset(self, dataset_label: str = "train") -> None:
        """Perform Principal Component Analysis of a dataset."""
        latent_data = []
        self.model.to("cpu")
        self.model.eval()

        # Extract the latent output from the encoder part of the model
        for d in self.datasets[dataset_label]:
            latent_representation = self.model.encoder(d)
            array = latent_representation.cpu().detach().numpy()
            latent_data.append(array)

        latent_data = np.vstack(latent_data)

        # Determine the PCA of the training sample in latent space
        pca = PCA(n_components=2, svd_solver="full")
        self.pca_fit = pca.fit(latent_data)
        self.pca_data = self.pca_fit.transform(latent_data)

    def record_session(self, output_prefix: str | None = None):
        """Save model + training metadata to file."""
        if output_prefix is None:
            model_name = type(self.model).__name__
            loss_name = type(self.loss).__name__
            optim_name = type(self.optim).__name__
            output_prefix = (
                f"{model_name}_{loss_name}_{optim_name}_trained_on_"
                f"{self.current_dataset}"
            )

        self.save_trained_model(output_name=output_prefix + ".pt")
        self.save_training_metadata(output_name=output_prefix + "_metadata.pt")
        self.save_pca(output_name=output_prefix + "_pca.pt")

    def save_pca(self, output_name: str) -> None:
        """Save the PCA fit + data from the training set."""
        self.fit_pca_to_dataset(dataset_label="train")
        torch.save([self.pca_fit, self.pca_data], output_name)
        logger.info(f"Saved PCA data to {output_name}.")
