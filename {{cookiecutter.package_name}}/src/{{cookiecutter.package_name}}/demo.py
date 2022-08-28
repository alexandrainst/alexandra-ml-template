"""Demo module."""

from pathlib import Path

import hydra
from omegaconf import DictConfig


@hydra.main(config_path="config", config_name="config")
def demo_function(config: DictConfig):
    """A demo function."""

    raw_path = Path(config.raw.path)
    print(f"Process data using {raw_path}")
