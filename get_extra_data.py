import json

import requests
import time

import re

from bs4 import BeautifulSoup


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
            value = sanitize_whitespace(prop.find('div', class_="v").text)
            props[key] = value

    coord_x, coord_y = parse_coordinates(soup)
    props["x"] = coord_x
    props["y"] = coord_y
    return props

if __name__ == "__main__":
    with open("data/full_list.json", "r") as full_list:
        data = json.loads(full_list.read())
        aids = [row[0] for row in data if row[0] is not None]
    aids_to_fetch = sorted(aids, reverse=True)
    for aid in aids_to_fetch:
        response = requests.get("https://bostad.stockholm.se/Lista/details/?aid=%s" % aid)
        props = parse(response.content)
        print(aid, props)
        time.sleep(5)

