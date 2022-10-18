from pathlib import Path
from linc.convertion import convert_to_physical_units

from linc.models import DataFileU32, DataFile
from linc.parse.header import parse_header
from linc.parse.dataset import parse_dataset
from linc.parse.file import read_file_header_dataset

# from rich import print


def parse_file(file_path: str | Path):
    _p = Path(file_path)
    h, d = read_file_header_dataset(_p)
    header = parse_header(h.split(b"\r\n"))
    dataset = parse_dataset(d, header=header)

    file_u32 = DataFileU32(header = header, dataset = dataset)
    file = convert_to_physical_units(file_u32)

    

    
