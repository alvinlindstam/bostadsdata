import requests
import time

import os

from utils import BUILDING_TYPES, QUEUES, get_raw_list_file_path, YEARS, QUEUE_TIME_GROUPS


def _ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def fetch(queue, year, building_type, group):
    response = requests.post(
        'https://bostad.stockholm.se/statistik/RenderApartmentList/',
        json={
            "rooms": "",
            "area": "",
            "apartmentType": "Alla",
            "buildingType": BUILDING_TYPES[building_type],
            "queue": QUEUES[queue],
            "year": str(year),
            "group": group
        },
        stream=True
    )

    # Throw an error for bad status codes
    response.raise_for_status()
    file_path = get_raw_list_file_path(queue, year, building_type, group)
    print(file_path)
    _ensure_dir(file_path)
    with open(file_path, 'wb+') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


if __name__ == "__main__":
    for queue in QUEUES.keys():
        for year in YEARS:
            for building_type in BUILDING_TYPES.keys():
                for group in QUEUE_TIME_GROUPS:
                    fetch(queue, year, building_type, group)
                    time.sleep(0.2)

