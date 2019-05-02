# importing the requests library 
import json
import requests 
import warnings
import sys
import argparse
warnings.filterwarnings("ignore") 

parser=argparse.ArgumentParser(
    description='''A utility script to generate shipment exceptions data for a specific organization [using its organization code]''',
    epilog="""""")
parser.add_argument('-o', type=int, default=18495, dest='organizationCode', required='true')
args=parser.parse_args()

organizationCode = args.organizationCode
# 1st api-endpoint 
URL1 = "https://demo-api.iasdispatchmanager.com:8502/v1/bv/shipmentsummary"

# 2nd api-endpoint 
URL2 = "https://demo-api.iasdispatchmanager.com:8502/v1/bv/shipments/e2eshipments"

# URL2 = "https://demo-api.iasdispatchmanager.com:8502/v1/bv/shipmentlist"


# Geocode address using google API
URL3 = "https://maps.googleapis.com/maps/api/geocode/json"

#Google API key
apiKey = "AIzaSyDw_5aG9oOfvJLgPMigMIz-vgTmPzgb3LY"
  
PARAMS1 = {'organizationCode':organizationCode} 
  
r1 = requests.get(url = URL1, params = PARAMS1, verify=False)
data = r1.json() 
totalExceptionCount = data['totalExceptionCount']
print('********API1 Executed******** totalExceptionCount', totalExceptionCount )

startRow = 0
endRow = totalExceptionCount
PARAMS2 = {'organizationCode':organizationCode, 'startRow': startRow, 'endRow': endRow, 'viewType': 'EXCEPTION' } 
r2 = requests.get(url = URL2, params = PARAMS2, verify=False) 
shipmentsData = r2.json() 
print('********API2 Executed******** shipmentsData', shipmentsData )
# print('********API2 Executed******** shipmentsData' )

data_list = []
for  ind, data in enumerate(shipmentsData):
    print('Hi *************',data)
    address = data['activeShipment']['destination']
    region = data['activeShipment']['destinationCity']
    shipmentReferenceNumber = data['shipmentReferenceNumber']
    customer = data['consignee']
    drayTypeTemp = data['activeShipment']['legMode']
    if(drayTypeTemp=='DRAY'):
        drayType = 'Truck'
    if (data['activeShipment']['shipmentException']):
        exceptionType = data['activeShipment']['shipmentException']['exceptionType']
        exceptionMessage = data['activeShipment']['shipmentException']['exceptionNotes']
    try:
        GEOCODE_PARAMS = {'address': address + " " + region, 'key': apiKey} 
        r3 = requests.get(url = URL3, params = GEOCODE_PARAMS, verify=False) 
        geocodeData = r3.json() 
        latitude = geocodeData['results'][0]['geometry']['location']['lat']
        longitude = geocodeData['results'][0]['geometry']['location']['lng']

        data_formatted = {
            "shipmentNumber": shipmentReferenceNumber,
            "region": region,
            "latitude": latitude,
            "longitude": longitude,
            "customer": customer,
            "exceptionType": exceptionType,
            "exceptionMessage": exceptionMessage,
            "recommendation": " Data not available",
            "drayType": drayType
        }
        data_list.append(data_formatted)
        print('\n ****geocode data', data_formatted)
        print('Data collection successful')
    except:
        print('Erorr due to incorrect data')

with open('data.json', 'w') as outfile:  
    json.dump(data_list, outfile, indent=4,)

