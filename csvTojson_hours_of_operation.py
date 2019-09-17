import csv
import json
import json
import requests 
import warnings
import sys
import argparse
from pprint import pprint
from pymongo import MongoClient
warnings.filterwarnings("ignore") 


data = { 
    "City": "",
    "Region": "",
    "Terminal": "",
    "Terminal Operator": "",
    "Capacity": "",
     }

result = {
    'hitsCount': '',
    'openingHoursCount': ''
        }
     
all_data = []

apiKey = "AIzaSyDw_5aG9oOfvJLgPMigMIz-vgTmPzgb3LY"
# google place search API
URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# google place details API
URL1 = "https://maps.googleapis.com/maps/api/place/details/json"

totalcount = 0
hitsCount = 0
openingHoursCount = 0
masterData = []
with open('Drwery_Container_Terminals.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        data = { 
                "City": row[0],
                "Region": row[1],
                "Terminal": row[2],
                "Terminal_Operator": row[3],
                "Capacity": row[4]
                }
        mData = { 
            'city': '',
            'region': '',
            'terminal': '',
            'Terminal_Operator': '',
            'capacity': '',
            'googleJson': [],
            'placeSearchText': ''
            }
        placeSearchText = row[2] + ' ' + row[0]
        mData['city'] = row[0] 
        mData['region'] = row[1] 
        mData['Terminal_Operator'] = row[3] 
        mData['terminal'] = row[2] 
        mData['capacity'] = row[4] 
        mData['placeSearchText'] = placeSearchText 
        all_data.append(data)

        PARAMS = {  'input':placeSearchText, 
            'inputtype': 'textquery', 
            'key': apiKey
          } 
        r1 = requests.get(url = URL, params = PARAMS, verify=False)
        print '\n ****************************************************************\n'
        print '\nplace search text: ', placeSearchText ,'\n'
        data = r1.json() 

        candidates = []
        found_already = False
        for pid in data['candidates']:
            hitsCount += 1
            placeId = pid['place_id']
            print 'placeId: ', placeId, '\n'

            PARAMS1 = { 'placeid':placeId, 
                        'fields': 'formatted_address,name,rating,opening_hours,geometry,formatted_phone_number,website,address_component,place_id,url',
                        'key': apiKey } 
            r2 = requests.get(url = URL1, params = PARAMS1, verify=False)
            pData = r2.json() 
            if 'opening_hours' in  pData['result']:
                if (not found_already):
                    openingHoursCount += 1
                    found_already = False

            candidates.append(pData['result'])
            pprint(pData['result'])
            print '\n hitsCount: ', hitsCount, 'openingHoursCount ', openingHoursCount,'totalcount ',totalcount, '\n'
           
        mData['googleJson'] = candidates
        if ( totalcount == 30):
            break
        masterData.append(mData)
        result['hitsCount'] = hitsCount
        result['openingHoursCount'] = openingHoursCount


# with open('Drwery_Container_Terminals.txt', 'w') as outfile:
#     json.dump(all_data, outfile)

with open('data_hours_for_55ports.json', 'w') as outfile:  
    json.dump(masterData, outfile, indent=4,)


with open('results_hours_for_55ports.json', 'w') as outfile:  
    json.dump(result, outfile, indent=4,)
               