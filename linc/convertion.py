from email.policy import default
import numpy as np
import numpy.typing as npt

from .models import DataFileU32, DataFile, Channel, MeasurementTypeEnum

SQUARED_CHANNELS = [
    MeasurementTypeEnum.ANALOG_SQUARED,
    MeasurementTypeEnum.PHOTONCOUNTING_SQUARED,
]


def convert_to_physical_units(data_file: DataFileU32) -> DataFile:
    final_dataset = data_file.dataset.copy().astype(np.float64)

    squared_channels = list(
        filter(
            lambda c: c.device_id.type in SQUARED_CHANNELS, data_file.header.channels
        )
    )

    measurement_channels = list(
        filter(lambda c: c not in squared_channels, data_file.header.channels)
    )

    # print(f"sq channels: {squared_channels}")
    # print(f"meas channels: {measurement_channels}")

    # First iterate over normal channels
    for idx, channel in enumerate(measurement_channels):
        final_dataset[idx] = _to_physical(channel, data_file.dataset[idx])

    for idx, channel in enumerate(squared_channels):
        ...

    return DataFile(header=data_file.header, dataset=final_dataset)


def _to_physical(
    channel: Channel, dataset: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    match channel.device_id.type:
        case MeasurementTypeEnum.ANALOG:
            _d = (dataset * channel.dc_dr) / (
                channel.shots * (2**channel.adc_bits - 1)
            )
        case MeasurementTypeEnum.PHOTONCOUNTING:
            _d = (dataset * channel.adc_bits) / (
                channel.shots * (2**channel.adc_bits - 1)
            )
        case MeasurementTypeEnum.POWERMETER:
            _d = dataset / channel.shots # Just apply normalization
        case MeasurementTypeEnum.POWERMETER_PHOTODIODE:
            _d = dataset / channel.shots # Just apply normalization
        case default:
            raise ValueError(f"Channel not handled: {default}")

    return _d
