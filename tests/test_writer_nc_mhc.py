from pathlib import Path

from linc.write.writer_nc import write_nc_legacy

def test_nc_writer() -> None:
    meas_path = Path("tests") / "data" / "2022" / "08" / "08"
    meas_files = list(meas_path.glob("RM*"))

    write_nc_legacy(meas_files, "output.nc", {
        
    })
