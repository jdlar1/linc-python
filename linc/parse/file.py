from pathlib import Path
from typing import Any

from ..models import DataFileU32


# def parse_file(file_path: Path | str) -> DataFile:
#     with open(file_path, "rb") as f:
#         header, dataset = f.read().split(b"\r\n\r\n")
    
#     return dataset


def read_file_header_dataset(file_path: Path | str) -> tuple[bytes, bytes]:
    _p = Path(file_path)

    with open(_p, 'rb') as f:
        header, _, dataset = f.read().partition(b"\r\n\r\n")

    return header, dataset