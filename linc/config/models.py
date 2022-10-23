from typing import Any

from pydantic import BaseModel, Field


DEFAULT_ATTRS: dict[str, Any] = {"generated_by": "linc-python"}


class SubConfig(BaseModel):
    include_undefined_channels: bool = True
    default_channel_name_format: str = r"%wx%p%a"


class LidarChannels(BaseModel):
    nick: str
    link_to: str # The device ID


class LidarConfig(BaseModel):
    attrs: dict[str, Any] = DEFAULT_ATTRS
    channels: list[LidarChannels] = Field(default_factory=list)


class Config(BaseModel):
    lidar: LidarConfig = Field(default_factory=LidarConfig)
    config: SubConfig = Field(default_factory=SubConfig)


"""
DEFAULT_CONFIG: Config = {
    "lidar": {
        "attrs": {"converter": "linc"},
        "channels": [
            # {"wavelength": 532, "link_to": "BT0"},
            # {"wavelength": 532, "link_to": "S2A0"},
            # {"wavelength": 532, "link_to": "BT1"},
            # {"wavelength": 532, "link_to": "S2A1"},
        ],
    },
    "config": {
        "include_undefined_channels": True,
        "default_channel_name_format": r"%wx%p%a",
    },
}
"""
