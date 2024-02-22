"""File containing the training and testing classes.

They classes are used to schedule and coordinate an ML
training phase.
"""

import torch
from torch.utils.data import DataLoader


# Generic Train Test class. avoid changing this as much as possible
class AlgoTrainTest:
    """Wrapper class around training steps of a pytorch model."""

    def __init__(self, model, optimizer, loss_fn, device="cuda"):
        """Initialize the training class."""
        self.model = model.to(device)
        self.loss = loss_fn
        self.optim = optimizer
        self.device = device
        self.datasets = {}
        self.current_dataset = None
        self.rms_history = []
        self.gradients_history = []

        # In debug mode, fix the random seed
        # torch.manual_seed(0)
        # also avoid using non-deterministic algorithms when running  fx. convolutions:
        # torch.use_deterministic_algorithms(True)

        # record historic evolution of the training
        self.loss_history = []
        self.weights_history = []
        self.bias_history = []

        # Linear layer weights
        self.linweights = []
        self.linbias = []

        # store results of an evaluation
        self.eval_results = {}

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
        self.rms_history = []
        self.gradients_history = []

        for i in range(n_epochs):
            if (i + 1) % 10 == 0:
                print(f"Epoch: {i}")
                print("-------------------------")
            self._train_one_epoch()

        print("DONE. I am done training.")
        if autosave:
            self.save_trained_model()

    def save_trained_model(self, output_name: str | None = None) -> None:
        """Save the trained model to .pt format.

        - batch size
        - dataset name
        - learning rate
        - n_epochs
        """
        model_name = type(self.model).__name__
        loss_name = type(self.loss).__name__
        optim_name = type(self.optim).__name__

        if output_name is None:
            full_name = f"{model_name}_{loss_name}_{optim_name}_\
            trained_on_{self.current_dataset}.pt"
        else:
            full_name = output_name

        torch.save(self.model.state_dict(), full_name)


#####################################################
# Project specific class. This is where you can adapt
# the training algorithm to your needs


class {{cookiecutter.class_prefix}}TrainTest(AlgoTrainTest):
    """In case a project requires customize training.

    If the particular project needs more custom training style, it
    is recommended to create a seaparate project-specific test-train
    class that inherits the basics of the AlgoTrainTest class.

    One can therefter substitute basic functions with custom ones, such as
    train_one_epoch in this case.

    """

    def __init__(
        self,
        model,
        model_type,
        optimizer,
        loss_fn,
        device="cuda",
    ):
        """Initialize inherited class + extra parameters."""
        AlgoTrainTest.__init__(
            self, model=model, optimizer=optimizer, loss_fn=loss_fn, device=device
        )
        self.model_type = model_type

    def _train_one_epoch(self):
        """Override of the generic training.

        We override the generic training
        because we need to distinguish the process
        for the two types of models we train.
        """
        for databatch in self.datasets[self.current_dataset]:
            # reset optimizer
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

            # run a step of optimization
            self.optim.step()
