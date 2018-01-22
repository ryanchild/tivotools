#!/usr/local/bin/python3

"""
tivotools.py

utilities for querying, downloading and deleting shows on TiVo

Usage: tivotools.py [--config=<config_file>]

Options:
  --config=<config_file>  config yaml file [default: config.yaml]
"""

import xmltodict
import io
import time
import requests
import sys
import yaml
from requests.auth import HTTPDigestAuth
from docopt import docopt


def main(opts):

  config = yaml.load(open(opts['--config']))

  for tivo in config['tivos']:
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
      r = requests.get('https://%s/TiVoConnect' % tivo['address'], params=payload, auth=HTTPDigestAuth('tivo',tivo['mak']), verify=False)

      d = xmltodict.parse(r.text)
      num_retrieved = int(d['TiVoContainer']['ItemCount'])
      total_shows = int(d['TiVoContainer']['Details']['TotalItems'])

      shows += d['TiVoContainer']['Item']

      print("Retrieved %s of %d total shows" % (len(shows), total_shows))

      anchor_offset += num_shows_per_request

      time.sleep(1)

# thetvdb
# 1. look up tvdb id by Details/Title (seriesName) : /search/series
# 2. @"http://thetvdb.com/api/GetEpisodeByAirDate.php?apikey=%@&seriesid=%@&airdate=%@"

if __name__ == '__main__':
  sys.exit(main(docopt(__doc__)))
