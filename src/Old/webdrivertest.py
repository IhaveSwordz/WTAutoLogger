from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import re
import http.client
import json
f = f"https://warthunder.com/en/community/userinfo/?nick=Karkazz"
req = Request(
    url=f,
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

)
with urlopen(req, timeout=10) as f:
    html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    with open("test.html", "w") as f:
        f.flush()
        f.write(soup)
    print(soup)