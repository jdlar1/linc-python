from typing import Any, TypedDict

class SubConfig(TypedDict):
    include_undefined_channels: bool
    default_channel_name_format: str

class LidarChannels(TypedDict):
    wavelength: int
    link_to: str


class LidarConfig(TypedDict):
    attrs: dict[Any, Any]
    channels: list[LidarChannels]


class Config(TypedDict):
    lidar: LidarConfig
    config: SubConfig


__doc__ = r"""
Configuration file.

config.default_channel_name_format Tokens:
%w Wavelength (3-4 digits integer)
%p Polarization state  (o, p, s, r, l)
%a Adquisition mode (a, p, A, P)  A and P is for squared datasets

"""