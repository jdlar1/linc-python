from pathlib import Path
from linc.models import PolarizationEnum

from linc.parse.header import parse_header
from linc.parse.file import read_file_header_dataset


def test_read_header():
    path = Path("tests") / "data" / "2022" / "07" / "14" / "RS2271411.481095"
    h, _ = read_file_header_dataset(path)
    header = parse_header(h.split(b"\r\n"))

    assert header.location == "Medellin"
    assert list(map(lambda x: x.polarization, header.channels)) == [
        PolarizationEnum.PARALLEL,
        PolarizationEnum.PARALLEL,
        PolarizationEnum.CROSSED,
        PolarizationEnum.CROSSED,
    ]
