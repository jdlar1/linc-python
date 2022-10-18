from pdb import set_trace
import numpy as np
import numpy.typing as npt
from rich import print

from .models import Channel, DataFile, DataFileU32, DeviceId, MeasurementTypeEnum

SQUARED_CHANNELS = [
    MeasurementTypeEnum.ANALOG_SQUARED,
    MeasurementTypeEnum.PHOTONCOUNTING_SQUARED,
]


def convert_to_physical_units(data_file: DataFileU32) -> DataFile:
    final_dataset = data_file.dataset.copy().astype(np.float64)

    squared_channels = list(
        filter(
            lambda t: t[1].device_id.type in SQUARED_CHANNELS,
            enumerate(data_file.header.channels),
        )
    )

    measurement_channels = list(
        filter(
            lambda t: t[1].device_id.type not in SQUARED_CHANNELS,
            enumerate(data_file.header.channels),
        )
    )

    print()
    print(f"squared channels: {[c[1].device_id for c in squared_channels]}")
    print(f"measurement channels: {[c[1].device_id for c in measurement_channels]}")

    # First iterate over normal channels
    for idx, channel in measurement_channels:
        final_dataset[idx] = _to_physical(channel, final_dataset[idx])

    for idx, channel in squared_channels:
        final_dataset[idx] = _to_standard_deviation(
            channel,
            final_dataset[idx],
            # data_file.dataset[measurement_dataset_idx].astype(np.float64),
        )

    return DataFile(header=data_file.header, dataset=final_dataset)


def _to_physical(
    channel: Channel, dataset: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    match channel.device_id.type:
        case MeasurementTypeEnum.ANALOG:
            _d = (1000 * dataset * channel.dc_dr) / (
                channel.shots * (2**channel.adc_bits - 1)
            )
        case MeasurementTypeEnum.PHOTONCOUNTING:
            _d = (dataset * channel.adc_bits) / (
                channel.shots * (2**channel.adc_bits - 1)
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
    dataset: npt.NDArray[np.float64],
    # measurement_dataset: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
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
