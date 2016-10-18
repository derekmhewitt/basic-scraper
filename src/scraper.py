# -*- coding: utf-8 -*-
"""This is a simple data scraper for King County restraunt inspection
information.

Followed tutorial here:
https://codefellows.github.io/sea-python-401d4/assignments/tutorials/scraper.html

Looked at Mike's scraper for hints when mine was broken:
https://github.com/Mikekh84/basic-scraper"""

import requests
from bs4 import BeautifulSoup
import sys
import re

# I rewrote this and I can't figure out exactly why, but my rewrite doesn't
# work, and the code from the assignment does.  Argh~

# DOMAIN_NAME = "http://info.kingcounty.gov"
# PATH = "/health/ehs/foodsafety/inspections/Results.aspx"
# QUERY_PARAMS = {
#     "Output": "W",
#     "Business_Name": "",
#     "Business_Address": "",
#     "Longitude": "",
#     "Latitude": "",
#     "City": "Seattle",
#     "Zip_Code": "",
#     "Inspection_Type": "All",
#     "Inspection_Start": "1/1/2016",
#     "Inspection_End": "2/28/2016",
#     "Inspection_Closed_Business": "A",
#     "Violation_Points": "",
#     "Violation_Red_Points": "",
#     "Violation_Descr": "",
#     "Fuzzy_Search": "N",
#     "Sort": "B",
# }


# def get_inspection_page(**kwargs):
#     """Makes a query to the King County inspection page and returns the
#     results."""
#     url = DOMAIN_NAME + PATH
#     print(url)
#     params = QUERY_PARAMS.copy()
#     for key, val in kwargs.items():
#         if key in QUERY_PARAMS:
#             params[key] = val
#     print(params)
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     # with open("inspection_page.html") as file:
#     #     file.write(response.content)
#     return response.content

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'H'
}


def get_inspection_page(**kwargs):
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.content


def load_inspection_page(filename):
    """Opens the output of a previously saved query result."""
    if filename == 'file':
        filename = 'inspection_page.html'
    with open(filename) as file:
        content = file.read()
        return content


def parse_source(html, encoding="utf-8"):
    """Uses BeautifulSoup to do stuff."""
    parsed = BeautifulSoup(html, "html5lib", from_encoding=encoding)
    return parsed


def extract_data_listings(html):
    """extracts divs where the id matches PR(some junk)"""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(element):
    """finds table rows that have only two children"""
    is_tr = element.name == 'tr'
    td_children = element.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def clean_data(td):
    """cleans empty strings out of the data we've scraped"""
    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restraunt_metadata(element):
    """gets restraunt metadata from html inputs"""
    try:
        metadata_rows = element.find('tbody').find_all(
            has_two_tds, recursive=False)
    except AttributeError:
        metadata_rows = []
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val_cell))
    return rdata


def is_inspection_row(element):
    """given an html element, determine if it's a tr and if it is, if it's
    the first element in a set of inspection data"""
    is_tr = element.name == 'tr'
    if not is_tr:
        return False
    td_children = element.find_all('td', recursive=False)
    has_four = len(td_children) == 4
    try:
        this_text = clean_data(td_children[0]).lower()
    except TypeError:
        this_text = ''
    contains_word = 'inspection' in this_text
    does_not_start = not this_text.startswith('inspection')
    return is_tr and has_four and contains_word and does_not_start


def extract_score_data(element):
    inspection_rows = element.find_all(is_inspection_row)
    samples = len(inspection_rows)
    total = high_score = average = 0
    for row in inspection_rows:
        strval = clean_data(row.find_all('td')[2])
        try:
            intval = int(strval)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += intval
            high_score = intval if intval > high_score else high_score
    if samples:
        average = total / float(samples)
    data = {
        u'Average Score': average,
        u'High Score': high_score,
        u'Total Inspections': samples,
    }
    return data


if __name__ == '__main__':
    kwargs = {
        'Insepction_Start': "1/1/2014",
        'Inspection_End': "3/5/2014",
        "Zip_Code": "98109"
    }
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        html = load_inspection_page('inspection_page.html')
    else:
        html = get_inspection_page(**kwargs)
    doc = parse_source(html)
    listings = extract_data_listings(doc)
    for listing in listings[:50]:
        metadata = extract_restraunt_metadata(listing)
        score_data = extract_score_data(listing)
        print(score_data, metadata)
