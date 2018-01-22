#!/usr/local/bin/python3

import xmltodict
import io
import time
import requests
from requests.auth import HTTPDigestAuth


mak = '***REMOVED***'

shows = []
num_shows_per_request = 50
num_retrieved = num_shows_per_request
anchor_offset = 0
while num_retrieved == num_shows_per_request:
  payload = {
    'Command':'QueryContainer',
    'Container':'/NowPlaying',
    'Recurse':'Yes',
    'AnchorOffset':anchor_offset,
    'Details':'All',
    'ItemCount':num_shows_per_request
  }
  r = requests.get('https://192.168.84.130/TiVoConnect', params=payload, auth=HTTPDigestAuth('tivo',mak), verify=False)

  d = xmltodict.parse(r.text)
  num_retrieved = int(d['TiVoContainer']['ItemCount'])
  total_shows = int(d['TiVoContainer']['Details']['TotalItems'])

  shows += d['TiVoContainer']['Item']

  print("Retrieved %s of %d total shows" % (len(shows), total_shows))

  anchor_offset += num_shows_per_request

  time.sleep(1)
