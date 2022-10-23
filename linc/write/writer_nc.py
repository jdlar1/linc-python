from pdb import set_trace
import time
from typing import Any
import warnings
from collections.abc import Iterable
from pathlib import Path

import numpy as np
from cftime import date2num

from ..models import DataFile
from ..reader import read_file
from ..write.common import get_bin_width
from ..config import Config
from .common import get_merged_channel_config, format_channel

# FIXME: This is broken in this Netcdf4 version
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from netCDF4 import Dataset  # type: ignore


def write_nc_legacy(
    files: Iterable[Path | str],
    output_file: Path | str,
    config: Config | dict = Config(),
) -> None:
    _f = sorted(list(files))
    config = Config(**config) if isinstance(config, dict) else config

    first_file = read_file(_f[0])

    nc = Dataset(output_file, "w")
    nc.history = "Created " + time.ctime(time.time())

    bin_width = get_bin_width(first_file.header)

    time_dim = nc.createDimension("time", None)
    range_dim = nc.createDimension("range", first_file.dataset.shape[0])

    time_var = nc.createVariable("time", "f8", ("time",), compression="zlib")
    time_var.units = f"microseconds since {first_file.header.start_date.isoformat().replace('T', ' ')}"
    time_var.calendar = "gregorian"
    time_var[0] = date2num(first_file.header.start_date, units=time_var.units)

    range_var = nc.createVariable(
        "range", "f8", ("range",), compression="zlib", complevel=1
    )
    range_var[:] = np.arange(
        bin_width, bin_width * (first_file.dataset.shape[0] + 1), bin_width
    )

    if len(config.lidar.channels) == 0:
        channels_vars = create_channels_from_header(nc, first_file, config)
    else:
        # channels_vars = create_channels_from_config(nc, first_file, config) # TODO: Finish this implementation
        channels_vars = create_channels_from_header(nc, first_file, config)

    for idx_f, iter_file in enumerate(_f):
        current_file = read_file(iter_file)
        time_var[idx_f + 1] = date2num(
            current_file.header.start_date, units=time_var.units
        )
        for (channel_str, channel_var) in channels_vars:
            channel_var[idx_f + 1, :] = current_file.dataset[channel_str].values  # type: ignore

    nc.close()


def create_channels_from_header(
    nc: Any, data_file: DataFile, config: Config
) -> list[tuple[str, Any]]:
    channels_vars: list[tuple[str, Any]] = []
    for channel in data_file.header.channels:
        _c = get_merged_channel_config(channel, config)
        channel_str = format_channel(
            _c, format=config.config.default_channel_name_format
        )

        signal_var = nc.createVariable(
            f"signal_{channel_str}",
            "f8",
            ("time", "range"),
            compression="zlib",
        )
        signal_var[0, :] = data_file.dataset[channel_str]

        channels_vars.append((channel_str, signal_var))
    return channels_vars


def create_channels_from_config(nc: Any, data_file: DataFile, config: Config) -> list[Any]:
    channels_vars = []

    channels_vars: list[tuple[str, Any]] = []
    for channel in config.lidar.channels:
        channel_str = channel.nick

        signal_var = nc.createVariable(
            f"signal_{channel_str}",
            "f8",
            ("time", "range"),
            compression="zlib",
        )
        signal_var[0, :] = data_file.dataset[channel_str]

        channels_vars.append((channel_str, signal_var))
    return channels_vars
