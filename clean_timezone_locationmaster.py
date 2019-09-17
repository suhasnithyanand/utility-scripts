# importing the requests library 
import json
import requests 
import warnings
import sys
import argparse
from pprint import pprint
from pymongo import MongoClient
from timezonefinder import TimezoneFinder

warnings.filterwarnings("ignore") 

client = MongoClient('10.138.0.32:27017')
db=client.qa
locationCollection = db['BG_Platform_Location']
apiKey = "AIzaSyDw_5aG9oOfvJLgPMigMIz-vgTmPzgb3LY"


tf = TimezoneFinder(in_memory=True)

result = {
    'totalRowsCount': '',
    'latLngCount': '',
    'addressCount': '',
    'countryCount': '',
    'stateCount': '',
    'cityCount': '',
    'timezoneMatchCount': '',
    'timezoneCount': ''
        }

totalRowsCount = 0
latLngCount = 0
addressCount = 0
countryCount = 0
stateCount = 0
cityCount = 0
timezoneMatchCount = 0
timezoneCount = 0

for post in locationCollection.find({ "$and" : [ { "latitude": { "$exists": "true" }} , { "longitude": { "$exists": "true" }} ]}):
# for post in locationCollection.find( ):
    totalRowsCount +=1 
    
    if 'latitude'  and 'longitude' and 'timezone' in post:
        if post['longitude'] != '' and post['latitude'] != '':
            latLngCount +=1 
            pytimezone = tf.timezone_at(lng=post['longitude'], lat=post['latitude'])
            print('\n: latitude', post['latitude'] ,'\t', ' longitude', post['longitude'])
            print('\n: py timezone', pytimezone ,'\t', ' location timezone', post['timezone'])

            if pytimezone == post['timezone']:
                timezoneMatchCount +=1
    if 'timezone' in post:
        timezoneCount +=1 
    if 'address1' in post:
        addressCount +=1 
    if 'city' in post:
        cityCount +=1 
    if 'country' in post:
        countryCount +=1 
    if 'state' in post:
            stateCount +=1 

    print('\n ****************************************************************\n')
    print('\ntimezoneMatchCount ', timezoneMatchCount, '\t totalRowsCount ', totalRowsCount, '\t timezoneCount ', timezoneCount, '\t latLngCount ', latLngCount, '\t addressCount ', addressCount, '\t countryCount ', countryCount, '\t cityCount ', cityCount, '\t stateCount ', stateCount) 
    # pprint(data)

    result['timezoneMatchCount'] = timezoneMatchCount
    result['totalRowsCount'] = totalRowsCount
    result['latLngCount'] = latLngCount
    result['addressCount'] = addressCount
    result['countryCount'] = countryCount
    result['stateCount'] = stateCount
    result['cityCount'] = cityCount



with open('results2.json', 'w') as outfile:  
    json.dump(result, outfile, indent=4,)
               
