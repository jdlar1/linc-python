from enum import Enum
from datetime import datetime

import numpy as np
import pandas as pd
import numpy.typing as npt
from pydantic import BaseModel, validator


class LaserPolarizationEnum(str, Enum):
    NONE = "0"
    VERTICAL = "1"
    HORIZONTAL = "2"
    RIGHT_CIRCULAR = "3"
    LEFT_CIRCULAR = "4"


class PolarizationEnum(str, Enum):
    NONE = "o"
    PARALLEL = "p"
    CROSSED = "s"
    RIGHT_CIRCULAR = "r"
    LEFT_CIRCULAR = "l"


class MeasurementTypeEnum(str, Enum):
    ANALOG = "BT"
    PHOTONCOUNTING = "BC"
    ANALOG_SQUARED = "S2A"
    PHOTONCOUNTING_SQUARED = "S2P"
    POWERMETER_PHOTODIODE = "PD"
    POWERMETER = "PM"


class FileTypeEnum(str, Enum):
    RAW_SIGNAL = "RS"
    DARK_CURRENT = "DC"
    TELECOVER = "TC"
    DESPOLARIZATION = "DP"


class Laser(BaseModel):
    shots: int
    frecuency: int


class DeviceId(BaseModel):
    number: int
    type: MeasurementTypeEnum


class Channel(BaseModel):
    active: bool
    laser: int
    bins: int
    laser_polarization: LaserPolarizationEnum = LaserPolarizationEnum.NONE
    ptm_voltage: int
    binwidth: float
    wavelength: int
    polarization: PolarizationEnum = PolarizationEnum.NONE
    adc_bits: int
    shots: int
    dc_dr: float  # Discriminator level () or data range
    device_id: DeviceId

    class Config:
        allow_mutation = False


class Header(BaseModel):
    filename: str
    location: str
    start_date: datetime
    stop_date: datetime
    altitude: float
    longitude: float
    latitude: float
    zenit_angle: float
    azimuth_angle: float | None = None
    n_datasets: int
    lasers: list["Laser"]
    channels: list["Channel"]

    class Config:
        anystr_strip_whitespace = True  # remove trailing whitespace
        allow_mutation = False

    # TODO: write custom validator for channels with associated lasers
    # @validator('channels')
    # def check_laser_on_channel(cls, v, _):
    #     return v


class DataFileU32(BaseModel):
    header: Header
    dataset: pd.DataFrame

    @validator("dataset")
    def dataset_length_must_match_header(cls, v, values):
        _header: Header = values["header"]

        # Header shape: (datasets x max bin of single profile)
        header_shape = (
            max(map(lambda x: x.bins, _header.channels)),
            _header.n_datasets,
        )
        if v.shape != header_shape:
            raise ValueError(
                f"Header shape: {header_shape} does not match with dataset shape {v.shape}"
            )

        return v

    class Config:
        arbitrary_types_allowed = True
        allow_mutation = False


class DataFile(DataFileU32):
    dataset: pd.DataFrame
