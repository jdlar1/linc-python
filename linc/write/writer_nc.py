from pdb import set_trace
import time
import warnings
from collections.abc import Iterable
from pathlib import Path

import numpy as np
from cftime import date2num

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
    _f = list(files)
    config = Config(**config) if isinstance(config, dict) else config

    first_file = read_file(_f[0])

    nc = Dataset(output_file, "w")
    nc.history = "Created " + time.ctime(time.time())

    bin_width = get_bin_width(first_file.header)

    time_dim = nc.createDimension("time", None)
    range_dim = nc.createDimension("range", first_file.dataset.shape[1])

    time_var = nc.createVariable("time", "f8", ("time",), compression="zlib")
    time_var.units = f"microseconds since {first_file.header.start_date.isoformat().replace('T', ' ')}"
    time_var.calendar = "gregorian"
    time_var[0] = date2num(first_file.header.start_date, units=time_var.units)

    range_var = nc.createVariable(
        "range", "f8", ("range",), compression="zlib", complevel=1
    )
    range_var[:] = np.arange(
        bin_width, bin_width * (first_file.dataset.shape[1] + 1), bin_width
    )

    channels_vars = []
    for idx, channel in enumerate(first_file.header.channels):
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
        signal_var[0, :] = first_file.dataset[idx]

        channels_vars.append(signal_var)

    for idx_f, iter_file in enumerate(_f):
        current_file = read_file(iter_file)
        time_var[idx_f + 1] = date2num(
            current_file.header.start_date, units=time_var.units
        )
        for idx_c, channel in enumerate(current_file.header.channels):
           
            channels_vars[idx_c][idx_f + 1, :] = current_file.dataset[idx_c]  # type: ignore

    nc.close()


# TODO: Implement this function to be 3D dataset
def write_nc(
    files: Iterable[Path | str],
    output_file: Path | str,
    config: Config | dict = Config(),
) -> None:
    _f = list(files)
    config = Config(**config) if isinstance(config, dict) else config

    first_file = read_file(_f[0])

    nc = Dataset(output_file, "w")
    nc.history = "Created " + time.ctime(time.time())

    bin_width = get_bin_width(first_file.header)

    time_dim = nc.createDimension("time", None)
    channel_dim = nc.createDimension("channel", first_file.dataset.shape[0])
    range_dim = nc.createDimension("range", first_file.dataset.shape[1])

    time_var = nc.createVariable(
        "time", "f8", ("time",), compression="zlib", complevel=1
    )
    time_var.units = f"microseconds since {first_file.header.start_date.isoformat().replace('T', ' ')}"
    time_var.calendar = "gregorian"
    time_var[0] = date2num(first_file.header.start_date, units=time_var.units)

    channel_var = nc.createVariable(
        "channel", str, "channel"
    )
    channels_vars: list[str] = []
    for channel in first_file.header.channels:
        _c = get_merged_channel_config(channel, config)
        channel_str = format_channel(
            _c, format=config.config.default_channel_name_format
        )
        channels_vars.append(channel_str)
    channel_var[:] = np.array(channels_vars, dtype=object)

    range_var = nc.createVariable(
        "range", "f8", ("range",), compression="zlib", complevel=1
    )
    range_var[:] = np.arange(
        bin_width, bin_width * (first_file.dataset.shape[1] + 1), bin_width
    )

    signal_var = nc.createVariable("signal", "f8", ("time", "channel", "range"), compression="zlib", complevel=4)

    signal_var[0, :, :] = first_file.dataset

    # set_trace()
    for idx_f, iter_file in enumerate(_f):
        current_file = read_file(iter_file)
        time_var[idx_f + 1] = date2num(
            current_file.header.start_date, units=time_var.units
        )
        
        try:
            signal_var[idx_f + 1, :, :] = current_file.dataset
        except:
            raise NotImplementedError("To Implement in future versions")
            """
            This is difficult since channels could or not be defined in the first file
            (Apply for raman channels on MULHACEN Lidar)
            But it works well in LIMON and other lidars with constant number of channels
            """
        # for idx_c, channel in enumerate(current_file.header.channels):
        #     
        #     channels_vars[idx_c][idx_f + 1, :] = current_file.dataset[idx_c]  # type: ignore

    nc.close()
