import numpy as np

from ..models import Header


def parse_dataset(dataset_list: list[bytes], header: Header):
    datasets: list[np.ndarray] = []

    for idx, _line in enumerate(dataset_list):
        try:
            datasets.append(np.frombuffer(_line, dtype=np.uint32))
        except Exception as e:
            print(f"index: {idx}")
            print(_line)
            raise e
    return datasets
