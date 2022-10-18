from typing import TypeVar, Iterator


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


def safe_get_list(l: list[U], idx: int, default: U) -> U:
    try:
        return l[idx]
    except IndexError:
        return default
