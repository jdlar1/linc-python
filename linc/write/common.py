from ..models import Header


def compare_joinable_dataset(header1: Header, header2: Header) -> None:
    assert (
        header1.channels == header2.channels
    ), "While parsing a same dataset, channels most remain identical"

    assert (
        header1.location == header2.location
    ), "While parsing a same dataset, channels most remain identical"


def get_bin_width(header: Header) -> float:
    bw = header.channels[0].binwidth

    for channel in header.channels:
        if channel.binwidth != bw:
            raise ValueError("Not all bins have the same width")
    
    return bw