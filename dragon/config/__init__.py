from pathlib import Path
import yaml

## Get Config
with Path(__file__).parent.joinpath("config.yml").open() as cf:
    config = yaml.safe_load(cf)

__all__ = ["config"]
