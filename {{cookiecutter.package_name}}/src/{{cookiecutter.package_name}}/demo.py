"""Demo module."""

import hydra
from omegaconf import DictConfig
from pathlib import Path


@hydra.main(config_path="../config", config_name='main')
def demo_function(config: DictConfig):
    """A demo function."""

    raw_path = Path(config.raw.path)
    print(f"Process data using {raw_path}")


if __name__ == '__main__':
    demo_function()
