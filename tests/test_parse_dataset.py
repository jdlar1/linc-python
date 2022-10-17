from pathlib import Path
from pdb import set_trace

from linc.models import DataFileU32
from linc.parse.header import parse_header
from linc.parse.dataset import parse_dataset
from linc.parse.file import read_file_header_dataset

# from rich import print


def test_read_header():
    path = Path("tests") / "data" / "2022" / "07" / "14" / "RS2271411.481095"
    h, d = read_file_header_dataset(path)

    header = parse_header(h.split(b"\r\n"))
    dataset = parse_dataset(d, header=header)

    file = DataFileU32(header = header, dataset = dataset)
    print()
    print(file.dataset)

    
