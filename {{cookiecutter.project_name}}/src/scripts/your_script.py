"""Main script for your project."""

import hydra
from omegaconf import DictConfig

from {{ cookiecutter.project_name }}.your_module import example_function


@hydra.main(config_path="../../config", config_name="config", version_base=None)
def main(config: DictConfig) -> None:
    """Main function for your project."""
    example_function(config=config)


if __name__ == "__main__":
    main()
