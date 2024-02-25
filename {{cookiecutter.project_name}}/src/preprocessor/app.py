"""Example FastAPI preprocessing module.

Use this application to service an application
that requires data preprocessing, prior to inference.
"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
	"""Webhook landing page."""
	return {"message": "Welcome to the IoTML Preprocessing module"}


# List existing classes of models availables
@app.get("/preprocess_data")
def preprocess_data():
	"""Perform some Python-based transformations to incoming data.

	This is where you can copy the code from a training script,
	so that the same operations can be performed on new live
	data.
	"""
	return {"message": "Here be some preprocessed data."}
