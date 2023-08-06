import json
import os
import random
import shutil

import numpy as np
import pandas as pd

from .comparator_class import SolutionComparator


def _create_hotel_input(size):
    return [
        {
            "lat": (random.betavariate(3, 3) - 0.5) * 125,
            "lon": (random.betavariate(3, 3) - 0.5) * 300,
        }
        for _ in range(size)
    ]


def _create_hotel_filter_input(size):
    return [
        {
            "lat": (random.betavariate(3, 3) - 0.5) * 125,
            "lon": (random.betavariate(3, 3) - 0.5) * 300,
            "stars": np.linspace(0, 5, 11)[np.random.randint(11)],
            **_get_price_pair(),
        }
        for _ in range(size)
    ]


def _get_price_pair():
    prices = np.sort(np.random.exponential(70, size=2))
    return {"min_price": prices[0], "max_price": prices[1]}


class HotelSolutionComparator(SolutionComparator):
    @staticmethod
    def _get_input(size):
        return _create_hotel_input(size)

    @staticmethod
    def _dump_data(size, path):
        data_path = os.path.join("data", f"{size}.csv")
        shutil.copy(data_path, path)


class HotelFilterSolutionComparator(HotelSolutionComparator):
    @staticmethod
    def _get_input(size):
        return _create_hotel_filter_input(size)


def get_hotel_data(data_root="data"):
    os.makedirs(data_root, exist_ok=True)
    for data_size_k in [10, 20, 50, 100, 200, 500]:
        data_size = data_size_k * 1000
        dl_path = (
            "https://borza-hotelcom-data.s3.eu-central-1"
            f".amazonaws.com/challenge-{data_size}.csv"
        )
        df = pd.read_csv(dl_path)
        write_path = os.path.join(data_root, f"{data_size}.csv")
        df.to_csv(write_path, index=False)


def dump_hotel_input(size, path="inputs.json"):
    obj = _create_hotel_input(size)
    with open(path, "w") as fp:
        json.dump(obj, fp)


def dump_hotel_filter_input(size, path="inputs.json"):
    obj = _create_hotel_filter_input(size)
    with open(path, "w") as fp:
        json.dump(obj, fp)
