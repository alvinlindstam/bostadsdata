import json
import re

from bs4 import BeautifulSoup

from utils import (BUILDING_TYPES, QUEUE_TIME_GROUPS, QUEUES, YEARS,
                   get_raw_list_file_path)

MONTHS = [None, 'jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']


def sanitize_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip())


def parse_coordinates(soup):
    map = soup.find('div', id="objMap")
    if map:
        match = re.search(r'(\d+):(\d+)~RT90', str(map))
        if match:
            return int(match.group(1)), int(match.group(2))

    return None, None


def parse(html, building_type):
    soup = BeautifulSoup(html, 'html.parser')

    values = []
    for tr in soup.find('table').find('tbody').find_all('tr'):

        tds = list(tr.find_all('td'))
        row_values = [sanitize_whitespace(td.text) for td in tds]
        if row_values != ['Inga bostäder har förmedlats för kön under valt år']:
            [municipality, part_of_town, address, rooms, area, rent, floor, queued_since, type_, _link] = row_values
            link_href = tds[2].find('a').attrs["href"]
            aid_str = link_href.replace("/Lista/details/?aid=", "")
            aid = None if aid_str == '' else int(aid_str)
            values.append([aid, municipality, part_of_town, address, rooms, area, rent, floor, queued_since, type_, building_type])
    return values


if __name__ == "__main__":
    all_values = []
    for queue in QUEUES.keys():
        for year in YEARS:
            for building_type in BUILDING_TYPES.keys():
                for group in QUEUE_TIME_GROUPS:
                    file_path = get_raw_list_file_path(queue, year, building_type, group)
                    print(file_path)
                    with open(file_path, 'r') as file:
                        all_values += parse(file.read(), building_type=building_type)

    def key(row):
        aid, *rest = row
        return aid is None, aid, rest
    all_values.sort(key=key)
    first_line = True
    with open("data/full_list.json", "w+") as full_list:
        full_list.write("[\n")
        for v in all_values:
            if first_line:
                first_line = False
            else:
                full_list.write(",\n")
            full_list.write("  " + json.dumps(v, ensure_ascii=False))
        full_list.write("]\n")
