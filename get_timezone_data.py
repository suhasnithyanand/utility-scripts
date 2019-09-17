import requests
import urllib.request
import time
from bs4 import BeautifulSoup

page = requests.get('https://timezonedb.com/time-zones')

soup = BeautifulSoup(page.text, 'html.parser')

# table = soup.find(class_='default')

# elements = table.find('tbody')

table = soup.find('table')
table_rows = table.find_all('tr')

data = []

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    # print(row)
    data.append(row)

data.pop(0)

tdata = {
    'Country Code': "",
    'Country Name': "",
    'Time Zone': "" 
        }


timezonedata = dict([])

for td in data:
    tdata = { 'Country Code': "", 'Country Name': "", 'Time Zone': "" }
    tdata["Country Code"] = td[0]
    tdata["Country Name"] = td[1]
    tdata["Time Zone"]    = td[2]
    utcname = str(td[3])
    utcname = utcname.replace(" ", "")
    if utcname in timezonedata:
        timezonedata[utcname].append(tdata)
    else:
        timezonedata[utcname] = []
        timezonedata[utcname].append(tdata)

print(timezonedata)
