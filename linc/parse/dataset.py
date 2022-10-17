from typing import Any

import numpy as np
import numpy.typing as npt

from ..models import Header

def parse_dataset(dataset: bytes, header: Header) -> npt.NDArray[np.uint8]:
    dt = np.dtype(np.uint32)
    dt = dt.newbyteorder("<")

    max_length = max(map(lambda x: x.bins, header.channels))
    parsed = np.full((len(header.channels), max_length), fill_value=np.nan)

    for idx, channel in enumerate(header.channels):
        bytes_size = channel.bins * 4
        current_array = np.frombuffer(dataset, dtype=dt, count=channel.bins)
        parsed[idx, :current_array.shape[0]] = current_array

        *_, dataset = dataset[bytes_size:].partition(b"\r\n")

    return parsed