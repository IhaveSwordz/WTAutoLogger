from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import re
import http.client
import json

import urllib.request


# url = "https://warthunder.com/en/community/getclansleaderboard/dif/_hist/page/1/sort/dr_era5"
# url = "https://warthunder.com/en/community/getclansleaderboard/dif/_hist/page/1/sort/deaths_hist"
url = "https://warthunder.com/en/community/getclansleaderboard/dif/_hist/page/1/sort/'tag'=P1KE"
headers={
    'User-Agent': 'Mozilla/5.0'
}

with urlopen(Request(url, headers=headers)) as f:
    f: http.client.HTTPResponse = f
    out: dict = json.load(f)
    # the zero represents the first squadron in the list, so in this case AVR
    keys = out['data'][0].keys()
    for o in keys:
        pass
        # print(f"key: {o}; data: {out['data'][0]['tag']}")
    for i in range(len(out['data'])):
        print(f"data: {out['data'][i]['tag']}, pos: {out['data'][i]['pos']}")

# class Team:
#     def __init__(self, data):
