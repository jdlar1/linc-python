from typing import Any, TypeVar, Iterator

from linc.models import MeasurementTypeEnum


U = TypeVar("U")
T = TypeVar("T", str, bytes)


def split_seq(seq: list[T], sep: T) -> Iterator[list[T]]:
    start = 0
    while start < len(seq):
        try:
            stop = start + seq[start:].index(sep)
            yield seq[start:stop]
            start = stop + 1
        except ValueError:
            yield seq[start:]
            break


def safe_get_list(l: list[U], idx: int, default: U | None) -> U | None:
    try:
        return l[idx]
    except IndexError:
        return default


def to_acquisition_type_string(type: MeasurementTypeEnum) -> str:
    match type:
        case MeasurementTypeEnum.ANALOG:
            return 'a'
        case MeasurementTypeEnum.ANALOG_SQUARED:
            return 'A'
        case MeasurementTypeEnum.PHOTONCOUNTING:
            return 'p'
        case MeasurementTypeEnum.PHOTONCOUNTING_SQUARED:
            return 'P'
        case _:
            raise ValueError("Input type not supported")