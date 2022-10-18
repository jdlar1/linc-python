from pathlib import Path

from linc.write.writer_nc import write_nc

def test_nc_writer() -> None:
    meas_path = Path("tests") / "data" / "2022" / "07" / "14"
    meas_files = list(meas_path.glob("RS*"))

    write_nc(meas_files, "output.nc")
