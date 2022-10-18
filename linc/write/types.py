from typing import Any, TypedDict


class SubConfig(TypedDict):
    include_undefined_channels: bool

class LidarChannels(TypedDict):
    wavelength: int


class LidarConfig(TypedDict):
    attrs: dict[Any, Any]
    channels: list[LidarChannels]


class Config(TypedDict):
    lidar: LidarConfig
    config: SubConfig
