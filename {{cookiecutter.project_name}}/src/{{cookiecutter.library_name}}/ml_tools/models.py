"""File containing pytorch models.

This file contains model architectures
used in the project. Here are by default
some models which have been previously used

"""
import logging

import torch
import torch.nn as nn
import torch.nn.functional as F


logger = logging.getLogger(__name__)


#
# Example LSTM Cell
#
class {{ cookiecutter.class_prefix }}LSTM(nn.Module):
	def __init__(self, lookback_window, predict_window, n_hidden=None):
		"""Univariate LSTM prediction model.

		Parameters:
		---

		lookback_window: int
				number of earlier time steps per sequence

		predict_window: int
				number of steps ahead the prediciton must cover
		"""
		super({{ cookiecutter.class_prefix }}LSTM, self).__init__()

		if n_hidden is None:
			n_hidden = lookback_window
		self.lstm = nn.LSTM(input_size=lookback_window, hidden_size=n_hidden)
		self.linear = nn.Linear(n_hidden, predict_window)

	def forward(self, x):
		"""Forward pass on the model."""
		output, (final_hidden_state, final_cell_state) = self.lstm(x)
		x = self.linear(output)
		return x


#
# Autoencoders for anomaly detection
#
class {{ cookiecutter.class_prefix }}Encoder(nn.Module):
	def __init__(self, input_dims, latent_dims):
		"""encoder section of autoencoder model."""

		super({{ cookiecutter.class_prefix }}Encoder, self).__init__()
		self.linear1 = nn.Linear(input_dims, 56)
		self.linear2 = nn.Linear(56, latent_dims)

	def forward(self, x):
		"""Forward pass on the model."""

		x = torch.flatten(x, start_dim=1)
		x = F.relu(self.linear1(x))
		return self.linear2(x)


class {{ cookiecutter.class_prefix }}Decoder(nn.Module):
	def __init__(self, latent_dims, output_dims):
		"""decoder section of autoencoder model."""

		super({{ cookiecutter.class_prefix }}Decoder, self).__init__()
		self.linear1 = nn.Linear(latent_dims, 56)
		self.linear2 = nn.Linear(56, output_dims)

	def forward(self, x):
		"""Forward pass on the model."""

		x = torch.flatten(x, start_dim=1)
		x = F.relu(self.linear1(x))
		return self.linear2(x)


class {{ cookiecutter.class_prefix }}AE(nn.Module):
	def __init__(self, input_dims, input_window, latent_dims):
		"""Autoencoder model for anomaly detection."""

		super({{ cookiecutter.class_prefix }}AE, self).__init__()
		input_size = input_dims * input_window
		self.encoder = {{ cookiecutter.class_prefix }}Encoder(input_size, latent_dims)
		self.decoder = {{ cookiecutter.class_prefix }}Decoder(latent_dims, input_size)

	def forward(self, x):
		"""Forward pass on the model."""

		z = self.encoder(x)
		return self.decoder(z)


#
# Various types of loss functions
#
class CustomLoss(nn.Module):
	def __init__(self):
		"""Custom loss for output predictor.

		Calculate the maximum value of the last 
		three elements in the input sequence
		"""
		super(CustomLoss, self).__init__()

	def forward(self, predicted_output, input_sequence, true_output):
		"""Forward pass on the model."""
		
		last_three_max = torch.max(input_sequence[:, -10:], true_output)

		# Compute the squared difference between the predicted output and last_three_max
		loss = torch.sum((predicted_output - last_three_max) ** 2)

		return loss


class AsymmetricLoss(nn.Module):
	def __init__(self):
		"""Loss function that over penalizes underpredictions."""

		super(AsymmetricLoss, self).__init__()

	def forward(self, predicted_output, input_sequence, true_output):
		"""Forward pass on the model."""

		E = (predicted_output - true_output) / true_output
		negative = 100 * E[E < 0.0] ** 2.0
		positive = torch.abs(E[E > 0.0])
		loss = negative.mean() + positive.mean()

		return loss


