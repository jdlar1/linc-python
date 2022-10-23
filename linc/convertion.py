import numpy as np
import pandas as pd
import numpy.typing as npt

from .models import Channel, DataFile, DataFileU32, MeasurementTypeEnum
from .utils import device_id_to_str

SQUARED_CHANNELS = [
    MeasurementTypeEnum.ANALOG_SQUARED,
    MeasurementTypeEnum.PHOTONCOUNTING_SQUARED,
]


def convert_to_physical_units(data_file: DataFileU32) -> DataFile:
    final_dataset = data_file.dataset.copy()

    squared_channels = list(
        filter(
            lambda c: c.device_id.type in SQUARED_CHANNELS,
            data_file.header.channels,
        )
    )

    measurement_channels = list(
        filter(
            lambda c: c.device_id.type not in SQUARED_CHANNELS,
            data_file.header.channels,
        )
    )

    # First iterate over normal channels
    for channel in measurement_channels:
        channel_str = device_id_to_str(channel.device_id)
        final_dataset[channel_str] = _to_physical(channel, final_dataset[channel_str])

    for channel in squared_channels:
        channel_str = device_id_to_str(channel.device_id)
        final_dataset[channel_str] = _to_standard_deviation(
            channel,
            final_dataset[channel_str],
            # data_file.dataset[measurement_dataset_idx].astype(np.float64),
        )

    return DataFile(header=data_file.header, dataset=final_dataset)


def _to_physical(channel: Channel, dataset: pd.Series) -> pd.Series:
    match channel.device_id.type:
        case MeasurementTypeEnum.ANALOG:
            _d = (1000 * dataset * channel.dc_dr) / (
                channel.shots * (2**channel.adc_bits - 1)
            )
        case MeasurementTypeEnum.PHOTONCOUNTING:
            _d = (dataset) / (
                channel.shots
                * 1e6
                * channel.binwidth  # Microseconds conversion output in MHz
            )
        case MeasurementTypeEnum.POWERMETER:
            _d = dataset / channel.shots  # Just apply normalization
        case MeasurementTypeEnum.POWERMETER_PHOTODIODE:
            _d = dataset / channel.shots  # Just apply normalization
        case default:
            # _d = (dataset) / (channel.shots * (2**channel.adc_bits - 1))
            raise ValueError(f"Channel not handled: {default}")
    return _d


def _to_standard_deviation(
    channel: Channel,
    dataset: pd.Series,
    # measurement_dataset: npt.NDArray[np.float64],
) -> pd.Series:
    match channel.device_id.type:
        case MeasurementTypeEnum.ANALOG_SQUARED:
            _s = (
                (1000 * dataset * channel.dc_dr)
                / (channel.shots * (2**channel.adc_bits - 1))
                / np.sqrt(channel.shots - 1)
            )
        case MeasurementTypeEnum.PHOTONCOUNTING_SQUARED:
            _s = (
                (1000 * dataset * channel.dc_dr)
                / (channel.shots * (2**channel.adc_bits - 1))
                / np.sqrt(channel.shots)
            )
        case default:
            raise ValueError(f"Channel not handled: {default}")
    return _s
