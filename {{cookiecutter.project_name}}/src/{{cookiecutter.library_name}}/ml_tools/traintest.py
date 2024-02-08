""" File containing the training and testing
class used to schedule and coordinate an ML
training phase

"""
import torch
from torch.utils.data import DataLoader
import numpy as np


class AlgoTrainTest:
    def __init__(self, model, optimizer, loss_fn, device="cuda"):
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
        self.datasets[label] = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        self.current_dataset = label

    def _train_one_epoch(self):
        for databatch in self.datasets[self.current_dataset]:
            # get data onto computing device
            sequence, output = databatch
            sequence = sequence.to(self.device)
            output = output.to(self.device)

            # reset optimizer
            self.optim.zero_grad()

            # Reconstruct tensor
            expectation = self.model(sequence)

            # Compute the Loss
            # TODO: input to loss function is not generic
            loss = self.loss(expectation, output)  # , sequence)
            self.loss_history.append(loss.item())
            loss.backward()

            # run a step of optimization
            self.optim.step()

    def train(self, dataset_label="train", n_epochs=10, autosave=True):
        self.current_dataset = dataset_label
        self.loss_history = []
        self.rms_history = []
        self.gradients_history = []

        for i in range(n_epochs):
            if (i + 1) % 100 == 0:
                print(f"Epoch: {i}")
                print("-------------------------")
            self._train_one_epoch()

        print("DONE. I am done training.")
        if autosave:
            self.save_trained_model()

    def save_trained_model(self):
        """TODO, include in the name:

        - batch size
        - dataset name
        - learning rate
        - n_epochs
        """

        model_name = type(self.model).__name__
        loss_name = type(self.loss).__name__
        optim_name = type(self.optim).__name__

        full_name = f"{model_name}_{loss_name}_{optim_name}"
        full_name += f"_trained_on_{self.current_dataset}.pt"
        torch.save(self.model.state_dict(), full_name)
        return full_name

    def predict(self, x):
        """Not relevant for this model"""
        pass

    def eval_model(self, dataset_label="test"):
        """Define how you want to evaluate the model
        following the training
        """
        pass

