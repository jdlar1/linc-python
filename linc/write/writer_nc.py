from collections.abc import Iterable
from pathlib import Path
from pdb import set_trace

from netCDF4 import Dataset  # type: ignore

from ..reader import read_file
from .types import Config


DEFAULT_CONFIG: Config = {
    "lidar": {
        "attrs": {"converter": "linc"},
        "channels": [
            {"wavelength": 532},
            {"wavelength": 532},
            {"wavelength": 532},
            {"wavelength": 532},
        ],
    },
    "config": {"include_undefined_channels": True},
}


def write_nc(files: Iterable[Path | str], config: Config = DEFAULT_CONFIG) -> None:
    _f = list(files)

    # TODO: Test Numpy warning: "np.array size changed"

    # first_file = read_file(_f[0])

