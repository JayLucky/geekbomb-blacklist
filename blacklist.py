#!/usr/bin/python

import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from collections import OrderedDict

AGE = 15
BINANCE_BASE = "https://support.binance.com"
BINANCE_NEW  = "/hc/en-us/sections/115000106672-New-Listings"
DATEANDTIME  = datetime.utcnow()
APPSETTINGS = '/var/opt/ptfeeder/config/appsettings.json'
SOMDEFAULTS = ['DGD','TRIG','MTL','SWIFT','ARDR','SAFEX','BTA','DAR','DRACO','SLING','CRYPT','DOGE','UNO','SC','INCNT','NAUT','SJCX','NOTE','TKN','TIME']

def get_blacklist():
    bl = []
    hrefs = re.findall(r'<a href="(.*-Binance-Lists-(.*)-(.*)-)"', requests.get(BINANCE_BASE+BINANCE_NEW).text)
    for href in hrefs:
        soup = BeautifulSoup(requests.get(BINANCE_BASE+href[0]).text, 'html.parser')
        deltaDate = DATEANDTIME - datetime.strptime(soup.time['datetime'], '%Y-%m-%dT%H:%M:%SZ')
        if deltaDate.total_seconds() < AGE * 86400:
            bl.append(href[2])
        else:
            break
    return(bl)

def update_settings(blCoins):
    with open(APPSETTINGS) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
        data['General']['SomOnlyPairs'] = ','.join(SOMDEFAULTS)+','+','.join(blCoins)
    with open(APPSETTINGS,'w') as f:
        json.dump(data, f, indent=2)

def main():
    update_settings(get_blacklist())

if __name__ == '__main__':
    main()
