from pathlib import Path

import numpy as np
from linc.reader import read_file


def test_reader():
    meas_path = Path("tests") / "data" / "2022" / "07" / "14"
    meas_files = list(meas_path.glob("RS*"))

    rnd_files = np.random.choice(meas_files, 4)  # type: ignore

    for file in rnd_files:
        _f = read_file(file)

        assert not (_f.dataset == np.nan).all(), "All items in dataset are NAN"
        assert len(_f.header.channels) == 4, "Channels in dataset should be 4"
