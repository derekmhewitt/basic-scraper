# -*- coding: utf-8 -*-
"""This is a simple data scraper."""

DOMAIN_NAME = "http://info.kingcounty.gov"

PATH = "health/ehs/foodsafety/inspections/Results.aspx"

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

def get_inspection_page():
    """."""
