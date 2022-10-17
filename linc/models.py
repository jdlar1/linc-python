from enum import Enum
from datetime import datetime

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, validator, Field


class LaserPolarizationEnum(str, Enum):
    NONE = "0"
    VERTICAL = "1"
    HORIZONTAL = "2"
    RIGHT_CIRCULAR = "3"
    LEFT_CIRCULAR = "4"


class PolatizationEnum(str, Enum):
    NONE = "o"
    PARALLEL = "p"
    CROSSED = "s"
    RIGHT_CIRCULAR = "r"
    LEFT_CIRCULAR = "l"


class FileTypeEnum(str, Enum):
    RAW_SIGNAL = "RS"
    DARK_CURRENT = "DC"
    TELECOVER = "TC"
    DESPOLARIZATION = "DP"


class Laser(BaseModel):
    shots: int
    frecuency: int


class Channel(BaseModel):
    active: bool
    type: int
    laser: int
    bins: int
    laser_polarization: LaserPolarizationEnum = LaserPolarizationEnum.NONE
    ptm_voltage: int
    binwidth: float
    wavelength: int
    polatization: PolatizationEnum = PolatizationEnum.NONE
    adc_bits: int
    shots: int
    dc_dr: float  # Discriminator level () or data range
    device_id: str


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

    # TODO: write custom validator for channels with associated lasers
    # @validator('channels')
    # def check_laser_on_channel(cls, v, _):
    #     return v

class DataFileU32(BaseModel):
    header: Header
    dataset: npt.NDArray[np.uint8]

    @validator("dataset")
    def dataset_length_must_match_header(cls, v, values):
        _header: Header = values["header"]

        if _header.n_datasets != len(v):
            raise ValueError(f"Header n_datasets ({_header.n_datasets}) and dataset length ({v.shape[0]}) must match")
        
        return v
        
    class Config:
        arbitrary_types_allowed = True
