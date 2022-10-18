import time
import warnings
from collections.abc import Iterable
from pathlib import Path
from pdb import set_trace

import numpy as np
from cftime import date2index, date2num

from ..models import Channel
from ..reader import read_file
from ..utils import to_acquisition_type_string
from ..write.common import get_bin_width
from .types import Config

# FIXME: This is broken in this Netcdf4 version
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from netCDF4 import Dataset  # type: ignore


DEFAULT_CONFIG: Config = {
    "lidar": {
        "attrs": {"converter": "linc"},
        "channels": [
            {"wavelength": 532, "link_to": "BT0"},
            {"wavelength": 532, "link_to": "S2A0"},
            {"wavelength": 532, "link_to": "BT1"},
            {"wavelength": 532, "link_to": "S2A1"},
        ],
    },
    "config": {
        "include_undefined_channels": True,
        "default_channel_name_format": r"%wx%p%a",
    },
}


def write_nc(
    files: Iterable[Path | str],
    output_file: Path | str,
    config: Config = DEFAULT_CONFIG,
) -> None:
    _f = list(files)
    first_file = read_file(_f[0])

    nc = Dataset(output_file, "w")
    nc.history = "Created " + time.ctime(time.time())

    bin_width = get_bin_width(first_file.header)

    time_dim = nc.createDimension("time", None)
    range_dim = nc.createDimension("range", first_file.dataset.shape[1])

    time_var = nc.createVariable("time", "f8", ("time",))
    time_var.units = (
        f"microseconds since {first_file.header.start_date.isoformat().replace('T', ' ')}"
    )
    time_var.calendar = "gregorian"
    time_var[0] = date2num(first_file.header.start_date, units=time_var.units)

    # TODO: Verify if bin0 means bw or 0
    range_var = nc.createVariable("range", "f8", ("range",))
    range_var[:] = np.arange(
        bin_width, bin_width * (first_file.dataset.shape[1] + 1), bin_width
    )

    channels_vars = []

    for idx, channel in enumerate(first_file.header.channels):
        _c = get_merged_channel_config(channel, config)
        channel_str = format_channel(
            _c, format=config["config"]["default_channel_name_format"]
        )

        signal_var = nc.createVariable(f"signal_{channel_str}", "f8", ("time", "range"))
        signal_var[0, :] = first_file.dataset[idx]

        channels_vars.append(signal_var)


    for idx_f, iter_file in enumerate(_f):
        current_file = read_file(iter_file)
        time_var[idx_f + 1] = date2num(current_file.header.start_date, units=time_var.units)
        for idx_c, channel in enumerate(current_file.header.channels):
            _c = get_merged_channel_config(channel, config)
            channel_str = format_channel(
                _c, format=config["config"]["default_channel_name_format"]
            )

            channels_vars[idx_c][idx_f + 1, :] = current_file.dataset[idx_c] # type: ignore

    nc.close()


def get_merged_channel_config(channel: Channel, config: Config) -> Channel:
    channel_as_str = f"{channel.device_id.type}{channel.device_id.number}"
    channel_config = list(
        filter(lambda c: c["link_to"] == channel_as_str, config["lidar"]["channels"])
    )[0]

    return Channel(**channel.copy(update=channel_config).dict())  # type: ignore


def format_channel(channel: Channel, format: str) -> str:
    format = format.replace(r"%w", str(channel.wavelength))
    format = format.replace(r"%p", channel.polarization.value)
    format = format.replace(r"%a", to_acquisition_type_string(channel.device_id.type))
    format = format.replace(
        r"%i", f"{channel.device_id.type}{channel.device_id.number}"
    )

    return format
