from linc.convertion import convert_to_physical_units

from rich import print

def test_physical_units_converter(data_file_u32):
    phys = convert_to_physical_units(data_file_u32)
