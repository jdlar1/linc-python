import numpy as np

from .models import DataFileU32, DataFile, Channel


def convert_to_physical_units(data_file: DataFileU32) -> DataFile:
    final_dataset = data_file.dataset.copy().astype(np.float64)


    for idx, channel in enumerate(data_file.header.channels):
        match channel.type:

    

    return DataFile(header=data_file.header, dataset=final_dataset)
