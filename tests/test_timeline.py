from tests.conftest import carsim_dataset
import json


def test_timeline(carsim_dataset: str):
    with open(carsim_dataset, 'r') as f:
        data = json.load(f)
        print(data)

