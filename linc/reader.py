from pathlib import Path

from .convertion import convert_to_physical_units
from .models import DataFileU32, DataFile
from .parse.header import parse_header
from .parse.dataset import parse_dataset
from .parse.file import read_file_header_dataset


def read_file(file_path: str | Path) -> DataFile:
    _p = Path(file_path)
    h, d = read_file_header_dataset(_p)
    header = parse_header(h.split(b"\r\n"))
    dataset = parse_dataset(d, header=header)

    file_u32 = DataFileU32(header=header, dataset=dataset)
    file = convert_to_physical_units(file_u32)

    return file
