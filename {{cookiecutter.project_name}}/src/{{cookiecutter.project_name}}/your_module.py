"""An example module for your project."""

from omegaconf import DictConfig


def example_function(config: DictConfig) -> None:
    """An example function for your project.

    Args:
        config: The Hydra config for your project.
    """
    print("Hello World!")
    print(f"Your config is: {config}")
