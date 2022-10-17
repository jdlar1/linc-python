from pathlib import Path
from pdb import set_trace

from linc.config import get_config


def test_read_config():
    path = Path("tests") / "data" / "lidar-config.toml"
    config = get_config(path)

    assert "lidar" in config.dict().keys()


def test_read_config_default():
    config = get_config()

    assert "lidar" in config.dict().keys()
