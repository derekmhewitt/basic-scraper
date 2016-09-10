# -*- coding: utf-8 -*-
"""This is a simple data scraper."""
import requests
from bs4 import BeautifulSoup
import sys

DOMAIN_NAME = "http://info.kingcounty.gov"
PATH = "/health/ehs/foodsafety/inspections/Results.aspx"
QUERY_PARAMS = {
    "Output": "W",
    "Business_Name": "",
    "Business_Address": "",
    "Longitude": "",
    "Latitude": "",
    "City": "Seattle",
    "Zip_Code": "",
    "Inspection_Type": "All",
    "Inspection_Start": "1/1/2016",
    "Inspection_End": "8/30/2016",
    "Inspection_Closed_Business": "A",
    "Violation_Points": "",
    "Violation_Red_Points": "",
    "Violation_Descr": "",
    "Fuzzy_Search": "N",
    "Sort": "Business_Address",
}


def get_inspection_page(**kwargs):
    """Makes a query to the King County inspection page and returns the
    results."""
    url = DOMAIN_NAME + PATH
    params = QUERY_PARAMS.copy()
    for key, val in kwargs.items():
        if key in QUERY_PARAMS:
            params[key] = val
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open("inspection_page.html") as file:
        file.write(response.content)
        file.write(response.encoding)
    return response.content, response.encoding


def load_inspection_page(filename="inspection_page.html"):
    """Opens the output of a previously saved query result."""
    with open(filename):
        content, encoding = file.read(filename)
        return content, encoding


def parse_source(html, encoding="utf-8"):
    """Uses BeautifulSoup to do stuff, where stuff == some voodoo magic
    that I don't fully understand yet."""
    parsed = BeautifulSoup(html, "html5lib", from_encoding=encoding)
    return parsed


if __name__ == '__main__':
    kwargs = {
        'Insepction_Start': "1/1/2014",
        'Inspection_End': "3/3/2014",
        "Zip_Code": "98109"
    }
    if len(sys.argv) > 1 and sys.argv[1] == "file":
        html, encoding = load_inspection_page()
    else:
        print("here")
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    print(doc.prettify(encoding=encoding))
