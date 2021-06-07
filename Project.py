import pandas as pd
import requests
import csv

# setting variable for google key to get lat/long data
key = 'AIzaSyD1nEKqqX_1jWyP-XGg9huWYjTk_l1XlOg'


# reading in Diagnosis data and merging hospital location and diagnosis data
Hospital_ID_Indiana = pd.read_csv('/Projects/4DG/HOSPITAL_ID_2019.csv')

Hospital_ID_Indiana['Hosptial_name_city'] = Hospital_ID_Indiana['Hospital_Name'].map(str) + ' ' + Hospital_ID_Indiana['Hospital_City'].map(str)

for row in Hospital_ID_Indiana['Hosptial_name_city']:
    id_value = row[0]
    input = row.replace(' ', '+')
    response = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + input + '&key=' + key
    get_response = requests.get(response)
    json_home_call = get_response.json()
    lat = json_home_call['results'][0]['geometry']['location']['lat']
    lng = json_home_call['results'][0]['geometry']['location']['lng']

    # ingest new values into a new csv (id_value and lat and long)
    print(lat, lng, row, sep=",")


# in order to input the new values into a csv, I ran a terminal command: Project.py > hosplatlong.txt
# to generate a new csv with hospital name and latitude/longitude.

# Due to reading errors in Pandas regarding translation from .txt to .csv, I had to manually convert the .txt to a .csv in excel
# To facilitate ease of use, I will attach the new .csv in the github repo so you have easy access
hosptlatlong = pd.read_csv('/Users/kgidwani/Documents/Purdue/Current/BIOL_597/Projects/4DG/hosplatlong.csv', names=['Latitude', 'Longitude', 'Hospital_name_city'])

latitude = hosptlatlong['Latitude']
longitude = hosptlatlong['Longitude']

Hospital_ID_Indiana['Lat'] = latitude
Hospital_ID_Indiana['Long'] = longitude
Hospital_ID_Indiana.to_csv("HospLatLongID.csv", index=False, encoding='utf-8-sig')
