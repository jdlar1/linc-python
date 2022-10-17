from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel

from tomli import load


class LidarConfig(BaseModel):
    attrs: dict


class Config(BaseModel):
    lidar: LidarConfig


FALLBACK_CONFIG = Path(__file__).parent / "default-config.toml"
CURRENT_DIR_CONFIG = Path("./lidar-conf.toml")


@lru_cache
def get_config(file: Path | str | None = None) -> Config:

    if file is not None:
        _cf = Path(file)
        if _cf.exists():
            config_path = _cf
        elif CURRENT_DIR_CONFIG.exists():
            config_path = CURRENT_DIR_CONFIG
        else:
            config_path = FALLBACK_CONFIG
    else:
        config_path = FALLBACK_CONFIG

    with open(config_path, "rb") as f:
        settings_dict = load(f)

    return Config(**settings_dict)
