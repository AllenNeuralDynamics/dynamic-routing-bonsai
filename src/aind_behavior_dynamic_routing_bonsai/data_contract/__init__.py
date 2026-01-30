import os
import typing as t
from pathlib import Path

import contraqctor
import semver

from aind_behavior_dynamic_routing_bonsai import __semver__


def dataset(path: os.PathLike, version: str = __semver__) -> contraqctor.contract.Dataset:
    """
    Loads the dataset for the dynamic-routing-bonsai project from a specified version.

    Args:
        path (os.PathLike): The path to the dataset root directory.
        version (str): The version of the dataset to load. By default, it uses the package version.

    Returns:
        contraqctor.contract.Dataset: The loaded dataset.
    """
    ...
    raise NotImplementedError("Dataset loading is not yet implemented for this project.")


def render_dataset(version: str = __semver__) -> str:
    """Renders the dataset as a tree-like structure for visualization."""
    from contraqctor.contract.utils import print_data_stream_tree

    return print_data_stream_tree(dataset(Path("<RootPath>")), show_missing_indicator=False, show_type=True)
