import json
import requests 
import warnings
import sys
import argparse
from pprint import pprint
from pymongo import MongoClient
warnings.filterwarnings("ignore") 


#dark-sky
apiKey = "2af862c6a9be8746c9c5ab3912036042"

#time-request
URL = "https://api.darksky.net/forecast/" + apiKey + "/" + latitude +  "," + longitude + "," + timestamp

GET 