"""Main script for your project.

Usage:
    python src/scripts/your_script.py <config_key>=<config_value> ...
"""

from {{ cookiecutter.project_name }}.your_module import example_function

import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../../config", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function for your project.

    Args:
        config: The Hydra config for your project.
    """
    example_function(config=config)


if __name__ == "__main__":
    main()
