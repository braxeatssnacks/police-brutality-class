# SMALL AREA INCOME AND POVERTY ESTIMATES in 2013 (BALTIMORE vs. FERGUSON)
# URL source = http://www.census.gov/did/www/saipe/data/interactive/cedr/cdr.html?s_appName=saipe&map_yearSelector=2013&map_geoSelector=aa_c&menu=grid_proxy

# -*- coding: utf-8 -*-

import pprint as pp
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import vincent
from geolocation.google_maps import GoogleMaps

%matplotlib inline

# *************************************************************************** #

# table

inFile = "data.csv" # downloaded
df = pandas.read_csv(inFile)

df_work = df[["Year", "State", "State / County Name", "Median Household Income in Dollars"]]
df_work = df[["Year", "State", "State / County Name", "All Ages in Poverty Percent", "Median Household Income in Dollars"]]
df_work.columns = ["Year", "State", "County_Name", "Poverty_Percentage", "Median_Household_Income_in_Dollars" ]

# *************************************************************************** #

# state numeric codes

def remove_quotes(string):
    """Removes extraneous quotes"""
    quotes = ["'","\""]
    characters = list(string)
    for char in characters:
        if char in quotes:
            characters.remove(char)
    joined = "".join(characters)
    return joined

def remove_lead0s(string_code):
    """Removes leading 0s"""
    characters = list(string_code)
    if characters[0] == "0":
        characters.remove(characters[0])
    number = "".join(characters)
    return number
        
def state_numeric_codes(inFile):
    """Creates a dictionary to reference states by their federal numeric code according to the inFile"""
    with open(inFile, "r") as csvfile: 
        state_code_dict = {}
        descr = csvfile.readline()

        while descr != "":
            split_descr = descr.split(",")

            if len(split_descr) >= 3:
                state_name = split_descr[3]
                state_code = split_descr[1]

                new_name = remove_quotes(state_name)
                code = remove_quotes(state_code)
                new_code = remove_lead0s(code)

                state = state_name.split()
                if len(state) == 1:
                    state_code_dict[new_name] = int(new_code)
            descr = csvfile.readline()
        
    return state_code_dict

# store function as variable
state_numeric_codes = state_numeric_codes(inFile)

# *************************************************************************** #

# location research

def county_finder(address):
    """Finds county according to input address"""
    API_KEY = "AIzaSyDg_eQsP4a0wjWt-Fy0fZH5gvVc9o5ZxCg"

    google_maps = GoogleMaps(api_key=API_KEY)
    # sends search to Google Maps
    location = google_maps.search(location=address)
    user_location = location.first()

    areas = [administrative_area.name for administrative_area in user_location.administrative_area]
    area_admin_types = [administrative_area.area_type for administrative_area in user_location.administrative_area]

    A = (dict(zip(area_admin_types, areas)))
    # level 2 = county
    county = A["administrative_area_level_2"]
    county = county.decode("utf-8")

    return county

def state_finder(address):
    """Finds state according to input address"""
    API_KEY = "AIzaSyDg_eQsP4a0wjWt-Fy0fZH5gvVc9o5ZxCg"

    google_maps = GoogleMaps(api_key=API_KEY)
    # sends search to Google Maps
    location = google_maps.search(location=address)
    user_location = location.first()

    areas = [administrative_area.name for administrative_area in user_location.administrative_area]
    area_admin_types = [administrative_area.area_type for administrative_area in user_location.administrative_area]

    A = (dict(zip(area_admin_types, areas)))
    # level 1 = state
    state = A["administrative_area_level_1"]
    state = state.decode("utf-8")

    return state

def lat_long_coords(address):
    """Finds lat & long coordinates according to input address"""
    API_KEY = "AIzaSyDg_eQsP4a0wjWt-Fy0fZH5gvVc9o5ZxCg"

    google_maps = GoogleMaps(api_key=API_KEY)
    # sends search to Google Maps
    location = google_maps.search(location=address)
    user_location = location.first()

    latitude = user_location.lat
    longitude = user_location.lng
    coordinates = [latitude, longitude]

    return coordinates

