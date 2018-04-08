import requests
import time

import os

queues = {
    "sthlm": "Bostadskön"
}  # todo: fetch other queues
building_types = {
    "nyproduktion": "Endast nyproduktion",
    "ej_nyproduktion": "Utan nyproduktion"
}
years = range(2000, 2019)
groups = [
  "0-2",
  "2-4",
  "4-6",
  "6-8",
  "8-10",
  "10-12",
  "12-14",
  "14-16",
  "16-18",
  "18-20",
  "20 <",
]


def _data_file_path(queue, year, building_type, group):
    return 'data/%s/%s/%s/%s.html' % (queue, year, building_type, group)

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
            "buildingType": building_types[building_type],
            "queue": queues[queue],
            "year": str(year),
            "group": group
        },
        stream=True
    )

    # Throw an error for bad status codes
    response.raise_for_status()
    file_path = _data_file_path(queue, year, building_type, group)
    print(file_path)
    _ensure_dir(file_path)
    with open(file_path, 'wb+') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


if __name__ == "__main__":
    for queue in queues.keys():
        for year in years:
            for building_type in building_types.keys():
                for group in groups:
                    fetch(queue, year, building_type, group)
                    time.sleep(0.2)

