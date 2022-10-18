from pdb import set_trace
from math import isclose

import numpy as np
from linc.convertion import convert_to_physical_units


def test_physical_units_converter(data_file_u32):
    phys = convert_to_physical_units(data_file_u32)


    # Compare against Licel conversion 0.1% Precision
    assert isclose(phys.dataset[0, 0], 5.30002, rel_tol=0.001)
    assert isclose(phys.dataset[1, 0], 0.00123043, rel_tol=0.001)
    assert isclose(phys.dataset[2, 0], 5.16307, rel_tol=0.001)
    assert isclose(phys.dataset[3, 0], 0.00134486, rel_tol=0.001)

    # Compare against means 0.1% Precision
    assert isclose(np.nanmean(phys.dataset[0]), 5.366899761688869, rel_tol=0.001)
    assert isclose(np.nanmean(phys.dataset[1]), 0.0028920661940507273, rel_tol=0.001)
    assert isclose(np.nanmean(phys.dataset[2]), 5.164334079387157, rel_tol=0.001)
    assert isclose(np.nanmean(phys.dataset[3]), 0.001361043748758466, rel_tol=0.001)
