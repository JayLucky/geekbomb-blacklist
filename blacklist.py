#!/usr/bin/python

import re
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from collections import OrderedDict

#
# Update AGE to the number of days you wish to blacklist.
# Update APPSETTINGS to match your file location.
# Update SOMDEFAULTS to change the list of default coins.
#
################################################################################
AGE = 15
APPSETTINGS = '/var/opt/ptfeeder/config/appsettings.json'
SOMDEFAULTS = ['DGD','TRIG','MTL','SWIFT','ARDR','SAFEX','BTA','DAR','DRACO','SLING','CRYPT','DOGE','UNO','SC','INCNT','NAUT','SJCX','NOTE','TKN','TIME','BCC','DLT','HSR']

#
# Don't edit below unless you are familiar with Python!
# This pulls the list of newly added coins from Binance
# and only blacklists the coins that are under AGE days
# from the current UTC time the script is ran.
#
################################################################################
BINANCE_BASE = "https://support.binance.com"
BINANCE_NEW  = "/hc/en-us/sections/115000106672-New-Listings"
DATEANDTIME  = datetime.utcnow()

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
        data['General']['SomOnlyCoins'] = ','.join(SOMDEFAULTS)+','+','.join(blCoins)
    with open(APPSETTINGS,'w') as f:
        json.dump(data, f, indent=2)

def main():
    update_settings(get_blacklist())

if __name__ == '__main__':
    main()
