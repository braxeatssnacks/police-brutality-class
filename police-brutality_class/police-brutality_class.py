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

# *************************************************************************** #

# AREA INFORMATION

BALTIMORE_ADDRESS = "Baltimore, MD 21030" # Freddie Gray

baltimore_state = state_finder(BALTIMORE_ADDRESS)
baltimore_county = county_finder(BALTIMORE_ADDRESS)
baltimore_coords = lat_long_coords(BALTIMORE_ADDRESS)
maryland_code = state_numeric_codes[baltimore_state]

print(BALTIMORE_ADDRESS)
pp.pprint(baltimore_state + " (" + str(maryland_code) + ")" + ", " + baltimore_county)
print("coordinates:", baltimore_coords, "\n")

FERGUSON_ADDRESS = "Ferguson, MO 63135" # Mike Brown

ferguson_state = state_finder(FERGUSON_ADDRESS)
ferguson_county = county_finder(FERGUSON_ADDRESS)
ferguson_coords = lat_long_coords(FERGUSON_ADDRESS)
missouri_code = state_numeric_codes[ferguson_state]

print(FERGUSON_ADDRESS)
pp.pprint(ferguson_state + " (" + str(missouri_code) + ")" + ", " + ferguson_county)
print("coordinates:", ferguson_coords, "\n")

CLEVELAND_ADDRESS = "Cleveland, OH 44101" # Tamir Rice

cleveland_state = state_finder(CLEVELAND_ADDRESS)
cleveland_county = county_finder(CLEVELAND_ADDRESS)
cleveland_coords = lat_long_coords(CLEVELAND_ADDRESS)
ohio_code = state_numeric_codes[cleveland_state]

print(CLEVELAND_ADDRESS)
pp.pprint(cleveland_state + " (" + str(ohio_code) + ")" + ", " + cleveland_county)
print("coordinates:", cleveland_coords, "\n")

# *************************************************************************** #

# HOUSEHOLD INCOMES & POVERTY PERCENTAGES

# Baltimore
df_maryland = df_work[(df.State == maryland_code)]
idx = df_maryland.query("County_Name == 'Baltimore County'").index.tolist()

income_str = df_maryland["Median_Household_Income_in_Dollars"][idx]
income_str = "".join(income_str)

# convert to int
mny_chars = ["$",","]

splt = list(income_str)
for char in splt:
    if char in mny_chars:
        splt.remove(char)
income = int("".join(splt))

baltimore_income = income
percent_frame = df_maryland["Poverty_Percentage"][idx]
baltimore_percent = float(percent_frame)

print("%s's County Median Household Income: $" % ("BALTIMORE") + str(baltimore_income))
print("%s's County Population Percentage in Poverty: %%" % ("BALTIMORE") + str(baltimore_percent) + "\n")

# *************************************************************************** #

# Ferguson
df_missouri = df_work[(df.State == missouri_code)]
idx = df_missouri.query("County_Name == 'St. Louis County'").index.tolist()

income_str = df_missouri["Median_Household_Income_in_Dollars"][idx]
income_str = "".join(income_str)

# convert to int
mny_chars = ["$",","]

splt = list(income_str)
for char in splt:
    if char in mny_chars:
        splt.remove(char)
income = int("".join(splt))

ferguson_income = income
percent_frame = df_missouri["Poverty_Percentage"][idx]
ferguson_percent = float(percent_frame)

print("%s's County Median Household Income: $" % ("FERGUSON") + str(ferguson_income))
print("%s's County Population Percentage in Poverty: %%" % ("FERGUSON") + str(ferguson_percent) + "\n")

# *************************************************************************** #

# Cleveland
df_ohio = df_work[(df.State == ohio_code)]
idx = df_ohio.query("County_Name == 'Cuyahoga County'").index.tolist()

income_str = df_ohio["Median_Household_Income_in_Dollars"][idx]
income_str = "".join(income_str)

# convert to int
mny_chars = ["$",","]

splt = list(income_str)
for char in splt:
    if char in mny_chars:
        splt.remove(char)
income = int("".join(splt))

cleveland_income = income
percent_frame = df_ohio["Poverty_Percentage"][idx]
cleveland_percent = float(percent_frame)

print("%s's County Median Household Income: $" % ("CLEVELAND") + str(cleveland_income))
print("%s's County Population Percentage in Poverty: %%" % ("CLEVELAND") + str(cleveland_percent) + "\n")

# *************************************************************************** #

# table of information

cities = ["Baltimore", "Ferguson", "Cleveland"]
counties = [baltimore_county, ferguson_county, cleveland_county]
incomes = [baltimore_income, ferguson_income, cleveland_income]
percentages = [baltimore_percent, ferguson_percent, cleveland_percent]

i = {"City": pd.Series(cities), "County": pd.Series(counties), "Household Median Income": pd.Series(incomes), "Percentage of Population in Poverty": pd.Series(percentages)}
df_main = pd.DataFrame(i)

# ************************************************************************** #

# graph

ax = df_main[["County","Household Median Income"]].plot(kind='bar', title ="Household Median Income",figsize=(15,10),use_index=False)
ax.set_xlabel("County")
ax.set_ylabel("Income (in dollars)")
ax.plot()

ax2 = df_main[["County","Percentage of Population in Poverty"]].plot(kind='bar', title ="Poverty Percentages",figsize=(15,10),use_index=False)
ax2.set_xlabel("County")
ax2.set_ylabel("Population in Poverty (%)")
ax2.plot()

# ************************************************************************** #

# map display

vincent.core.initialize_notebook()

world_topo = r'https://github.com/trifacta/vega/blob/gh-pages/data/world-countries.json'
state_topo = r'https://github.com/trifacta/vega/blob/gh-pages/data/us-states.json'
county_geo = r'https://github.com/trifacta/vega/blob/gh-pages/data/us-counties.json'
county_topo = r'https://github.com/trifacta/vega/blob/gh-pages/data/us-counties.json'

geo_data = [{'name': 'counties',
             'url': county_topo,
             'feature': 'us_counties.geo'},
            {'name': 'states',
             'url': state_topo,
             'feature': 'us_states.geo'}
             ]

vis = vincent.Map(geo_data=geo_data, scale=1000, projection='albersUsa')
del vis.marks[1].properties.update
vis.marks[0].properties.update.fill.value = '#084081'
vis.marks[1].properties.enter.stroke.value = '#fff'
vis.marks[0].properties.enter.stroke.value = '#7bccc4'
vis.to_json('vega.json')

vis.display()
