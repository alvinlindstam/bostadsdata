import json

import requests
import time

import re

from bs4 import BeautifulSoup
from datetime import date

from utils import write_prettier_json


SHORTER_KEYS = {
    "Annons publicerad": "pub_d",
    "Anmälan senast": "ad_d",
    "fetch_date": "fd",
    "Inflyttning": "move_d",
    "Gatuadress": "addr",
    "Antal rum": "rooms",
    "Yta": "area",
    "Hyra": "rent",
    "Våning": "floor",
    "Lägenhetsnummer": "ap_no",
}


def sanitize_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip())


def parse_coordinates(soup):
    map = soup.find('div', id="objMap")
    if map:
        match = re.search(r'(\d+):(\d+)~RT90', str(map))
        if match:
            return int(match.group(1)), int(match.group(2))

    return None, None


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    props = {}
    for box_id in ["annons-top-bar", "objFacts"]:
        box = soup.find('div', id=box_id)
        for prop in box.find_all('div', class_="egenskap"):
            key = sanitize_whitespace(prop.find('div', class_="n").text)
            key = key.rstrip(':')
            key = SHORTER_KEYS.get(key, key)
            value = sanitize_whitespace(prop.find('div', class_="v").text)
            props[key] = value

    coord_x, coord_y = parse_coordinates(soup)
    props["x"] = coord_x
    props["y"] = coord_y

    landlord_link = soup.find('a', title="Hyresvärdens webbplats")
    if landlord_link:
        props['ll'] = str(landlord_link.attrs['href'])
    return props


if __name__ == "__main__":
    with open("data/full_list.json", "r") as full_list:
        data = json.loads(full_list.read())
        aids = set(row[0] for row in data if row[0] is not None)

    with open("data/extra_ad_data.json", "r") as old_extra_data:
        extra_data = json.loads(old_extra_data.read())
        existing_aids = set(int(aid) for aid in extra_data.keys())

    aids_to_fetch = aids - existing_aids
    counter = 0

    try:
        session = requests.Session()
        for aid in sorted(aids_to_fetch, reverse=True):
            response = session.get("https://bostad.stockholm.se/Lista/details/?aid=%s" % aid)
            assert response.status_code == 200
            props = parse(response.content)
            props[SHORTER_KEYS['fetch_date']] = date.today().isoformat()
            extra_data[str(aid)] = props
            print(aid, counter, round(counter/len(aids_to_fetch), 3))
            counter += 1
            time.sleep(0.05)
    finally:
        with open("data/extra_ad_data.json", "w+") as extra_data_file:
            write_prettier_json(extra_data, file=extra_data_file)

