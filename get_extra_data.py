import requests
import time

import os

from utils import BUILDING_TYPES, QUEUES, get_raw_list_file_path, years, QUEUE_TIME_GROUPS


import datetime
import re

from bs4 import BeautifulSoup
from .models import AdState, Apartment


MONTHS = [None, 'jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'okt', 'nov', 'dec']

def parse_datestring(datestring):
    if datestring:
        return datetime.datetime.strptime(datestring.strip(), "%Y-%m-%d").date()

def swe_float(input):
    return float(input.replace(',', '.'))

def sanitize_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip())

def get_project_apartments(soup):
    projObjlist = soup.find('table', class_='projObjlist')
    if not projObjlist:
        return []

    apartments = []
    for projObj in projObjlist.tbody.find_all('tr'):
        tds = [td.text.strip() for td in projObj.find_all('td')]

        assert len(tds) == 8
        apartment = Apartment(
            apartment_no=tds[0],
            address=tds[1],
            floor=tds[2],
            area=swe_float(tds[3]),
            rent=int(tds[4]),
            rooms=swe_float(tds[5]),
            available_from=parse_datestring(tds[6])
        )
        apartments.append(apartment)
    return apartments

def get_non_project_apartment(soup):
    objFacts = soup.find('div', id='objFacts')
    aparment = Apartment()
    for factList in objFacts.find_all('ul', class_='list'):
        factList_lis = factList.find_all('li', recursive=False)
        for i in range(0, len(factList_lis), 2):
            title = factList_lis[i].text.strip()
            value = factList_lis[i + 1].text.strip()
            if title == 'Adress:':
                aparment.address = value
            elif title == 'Antal rum:':
                value = re.match('([0-9,])+(\sRitning)?', value).group(1)
                aparment.rooms = swe_float(value)
            elif title == 'Yta:':
                value = re.match('([0-9,]*)\s?m²', value).group(1)
                if value:
                    aparment.area = swe_float(value)
            elif title == 'Hyra:':
                value = re.match('([0-9,]*)\s?kr/mån', value).group(1)
                if value:
                    aparment.rent = int(value)
            elif title == 'Våning:':
                aparment.floor = value
            elif title == 'Inflyttning:':
                # Todo add to model
                pass#aparment.
            elif title == 'Lägenhetsnummer:':
                aparment.apartment_no = value
            else:
                print('unknown title', title, value)
    return aparment


def parse_header(ad, queue_text):
    queue_text = sanitize_whitespace(queue_text)
    if 'För att anmäla intresse' in queue_text:
        ad.ad_state = AdState.open
    elif queue_text == 'Annonsen är avregistrerad':
        ad.ad_state = AdState.removed
    elif queue_text == 'Annonseringen är avslutad':
        # Seems like project pages stay with this status, without information about queue times.
        ad.ad_state = AdState.closed
    elif 'Bostaden är förmedlad' in queue_text:
        ad.ad_state = AdState.assigned

        queue_time = re.search(r'Kötid\: (\w+) (\d+)', queue_text)
        if queue_time:
            return datetime.date(
                year=int(queue_time.group(2)),
                month=MONTHS.index(queue_time.group(1)),
                day=1
            )
    else:
        ad.ad_state = AdState.unknown
        print(queue_text, 'unknown status header', ad.bis_id)

    return None

def parse_coordinates(soup):
    map = soup.find('div', id="objMap")
    if map:
        match = re.search(r'(\d+):(\d+)~RT90', str(map))
        if match:
            return int(match.group(1)), int(match.group(2))

    return None, None

def parse(html=None):
    soup = BeautifulSoup(html, 'html.parser')

    props = {}
    for box_id in ["annons-top-bar", "objFacts"]:
        box = soup.find('div', id=box_id)
        for prop in box.find_all('div', class_="egenskap"):
            key = prop.find('div', class_="n").text
            value = prop.find('div', class_="v").text
            props[key] = value


    props = [sanitize_whitespace(node.text) for node in header.find_all(class_='egenskap')]

    coord_x, coord_y = parse_coordinates(soup)
    props["coord_x"] = coord_x
    props["coord_y"] = coord_y
    print(props)


if __name__ == "__main__":
    for queue in QUEUES.keys():
        for year in years:
            for building_type in BUILDING_TYPES.keys():
                for group in QUEUE_TIME_GROUPS:
                    parse(queue, year, building_type, group)

