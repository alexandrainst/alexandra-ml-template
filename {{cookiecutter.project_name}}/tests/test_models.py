"""Example test script for the project's
model class.
"""
import torch
from {{ cookiecutter.library_name }}.ml_tools.models import {{ cookiecutter.class_prefix }}AE
from {{ cookiecutter.library_name }}.ml_tools.models import {{ cookiecutter.class_prefix }}LSTM

def test_lstm():
	m = {{ cookiecutter.class_prefix }}LSTM(predict_window=1, lookback_window=4)
	x_example = torch.Tensor([4.0, 35.0, 3.0, -4])
	x_example = torch.unsqueeze(x_example, dim=0)
	x_example = torch.unsqueeze(x_example, dim=0)
	print(m(x_example))


def test_autoencoder():
	m = {{ cookiecutter.class_prefix}}AE(input_window=100, input_dims=2, latent_dims=33)
	print("model:\n------------------\n", m)
	# example of a batch of 34 input time series
	x = torch.zeros([34, 1, 200])
	print(f"\n-------------------\n\nfull model output shape: {m(x).shape}")
	print(f"\n-------------------\n\nencoder model output shape: {m.encoder(x).shape}")

	# latent space example for a batch of 34 time series
	latent_x = torch.zeros([34, 33])
	print(
		f"\n-------------------\n\n \
		decoder model output shape: {m.decoder(latent_x).shape}"
	)


if __name__ == "__main__":
	test_autoencoder()
	test_lstm()
