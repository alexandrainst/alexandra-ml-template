"""Example test script for the project's dataset class."""

from {{ cookiecutter.library_name }}.ml_tools.datasets import {{ cookiecutter.class_prefix }}Dataset


def test_datasets():
    """Load a dataset class and loop through some events."""
    model_params = {"input_dims": 2, "input_window": 10}
    d = {{ cookiecutter.class_prefix }}Dataset(
        model_params=model_params,
        dataset_path="./path_to_your_dataset",
    )
    print(len(d))
    for e in d:
        print(e)
        break


if __name__ == "__main__":
    test_datasets()
