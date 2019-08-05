# importing the requests library 
import json
import requests 
import warnings
import sys
import argparse
from pprint import pprint
from pymongo import MongoClient
warnings.filterwarnings("ignore") 

# 'fields': 'photos,formatted_address,name,rating,opening_hours,geometry',


client = MongoClient('10.138.0.32:27017')
# Set the db object to point to the business database
db=client.conv
locationCollection = db['BG_Platform_Location']
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)
# AIzaSyDw_5aG9oOfvJLgPMigMIz-vgTmPzgb3LY
#Google API key
# apiKey = "AIzaSyCVJ_4G85silDMaq9tlOz-mLGzGmc5ypII"
apiKey = "AIzaSyDw_5aG9oOfvJLgPMigMIz-vgTmPzgb3LY"
# google place search API
URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# google place details API
URL1 = "https://maps.googleapis.com/maps/api/place/details/json"

masterData = []

 
result = {
    'noPlaceNameCount': '',
    'noAddressCount': '',
    'hitsCount': '',
    'openingHoursCount': ''
        }

locationType = ['DC', 'AIRPORT', 'RAMP', 'MML', 'RAIL_YARD', 'PORT', 'BORDER']
locationType = ['RAMP', 'PORT',]

noPlaceNameCount = 0
noAddressCount = 0
hitsCount = 0
openingHoursCount = 0

totalcount = 0

for post in locationCollection.find({ "$and" : [ { "$or": [ { 'locationType.name': 'PORT' } ] },{'country':'US'} ] }):
    totalcount +=1 
    mData = { '_id': '',
            'active': '',
            'city': '',
            'code': '',
            'codeType': '',
            'country': '',
            'createDate': '',
            'createUser': '',
            'customCode': '',
            'customCodeType': '',
            'latitude': '',
            'locationType': '',
            'longitude': '',
            'name': '',
            'sourceApplication': '',
            'state': '',
            'timezone': '',
            'updateDate': '',
            'updateUser': '',
            'version': '',
            'googleJson': [],
            'placeSearchText': ''
            }
    if post['locationType']['name'] in locationType:
        #print post['locationType']['name']

        mData['_id'] = post['_id']
        if 'latitude' in post:
            mData['latitude'] = post['latitude']
        if 'longitude' in post:
            mData['longitude'] = post['longitude']
        if 'timezone' in post:
            mData['timezone'] = post['timezone']
        if 'codeType' in post:
            mData['codeType'] = post['codeType']

        if 'name' in post:
            placeName = post['name']
            mData['name'] = post['name']
        else:
            placeName = ' '
            noPlaceNameCount += 1
        if 'address1' in post:
            address = post['address1']
            mData['address'] = post['address1']
        if 'city' in post:
            city = post['city'] or ' '
            mData['city'] = post['city']  or ' '
        if 'country' in post:
            country = post['country'] or ' '
            mData['country'] = post['country']  or ' '
        if 'state' in post:
            state = post['state'] or ' '
            mData['state'] = post['state']  or ' '

        if 'address1' in post:
            placeSearchText = placeName + ' ' + address + ' ' + city + ' ' + state + ' ' + country
            mData['placeSearchText'] = placeSearchText
        else:    
            placeSearchText = placeName + ' ' + city + ' ' + state + ' '  + country
            noPlaceNameCount += 1
            mData['placeSearchText'] = placeSearchText


        PARAMS = {  'input':placeSearchText, 
            'inputtype': 'textquery', 
            'key': apiKey
          } 
        r1 = requests.get(url = URL, params = PARAMS, verify=False)
        print '\n ****************************************************************\n'
        print '\nplace name: ', placeName
        print '\nplace search text: ', placeSearchText ,'\n'
        data = r1.json() 
        # pprint(data)

        candidates = []
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
                openingHoursCount += 1

            candidates.append(pData['result'])
            pprint(pData['result'])
            print '\n noPlaceNameCount: ', noPlaceNameCount, 'noAddressCount: ', noAddressCount, 'hitsCount: ', hitsCount, 'openingHoursCount ', openingHoursCount,'totalcount ',totalcount, '\n'
           
        mData['googleJson'] = candidates
        if ( totalcount == 30):
            break
    masterData.append(mData)
    result['noPlaceNameCount'] = noPlaceNameCount
    result['noAddressCount'] = noAddressCount
    result['hitsCount'] = hitsCount
    result['openingHoursCount'] = openingHoursCount
  


with open('data1.json', 'w') as outfile:  
    json.dump(masterData, outfile, indent=4,)


with open('results1.json', 'w') as outfile:  
    json.dump(result, outfile, indent=4,)
               
