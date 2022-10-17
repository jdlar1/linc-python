from pathlib import Path
from linc.models import PolatizationEnum

from linc.parse.header import parse_header
from linc.parse.file import read_file_header_dataset

from rich import print


def test_read_header():
    path = Path("tests") / "data" / "2022" / "07" / "14" / "RS2271411.481095"
    h, _ = read_file_header_dataset(path)
    header = parse_header(h.split(b"\r\n"))

    print(header)

    assert header.location == "Medellin"
    assert list(map(lambda x: x.polatization, header.channels)) == [
        PolatizationEnum.PARALLEL,
        PolatizationEnum.PARALLEL,
        PolatizationEnum.CROSSED,
        PolatizationEnum.CROSSED,
    ]
