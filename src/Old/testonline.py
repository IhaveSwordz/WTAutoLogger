import urllib.request
import http.client
import urllib.request
import socket
import json
import time

import requests


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8111))
    s.send(b"GET /mission.json HTTP/1.1\r\nHost:localhost:8111\r\nConnection: keep-alive\r\n\r\n\r\n")
    out = s.recv(10000).decode("utf-8")
    out = json.loads(out[out.index("\r\n\r\n"):])
    # indicators = out["valid"]
    s.close()
    time.sleep(0.1)
    print(out)
'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8111))
    s.send(b"GET /state HTTP/1.1\r\nHost:localhost:8111\r\nConnection: keep-alive\r\n\r\n\r\n")
    out = s.recv(10000).decode("utf-8")
    out = json.loads(out[out.index("\r\n\r\n"):])
    state = out["valid"]
    s.close()
    print(f"indicators: {indicators}; state: {state}")
    # print(out)'''

'''
while True:
    h1 = http.client.HTTPConnection('localhost:8111')
    while True:
        try:
            print(h1.getresponse())
        except:
            pass

    print("-"*50+"\n"+"Reading State: \n")
    with urllib.request.urlopen("http://localhost:8111/state") as f:
        print(f.read())

    print("-"*50+"\n"+"Reading indicators: \n")
    with urllib.request.urlopen(("http://localhost:8111/indicators")) as f:
        print(f.read())'''
'''
s = requests.Session()

def streaming(symbols):
    payload = {'symbols': ','.join(symbols)}
    headers = {'connection': 'keep-alive', 'content-type': 'application/json', 'x-powered-by': 'Express', 'transfer-encoding': 'chunked'}
    req = requests.Request("GET",'http://localhost:8111/indicators',
                           headers=headers).prepare()

    while True:
        resp = s.send(req, stream=True)

        for line in resp.iter_lines():
            if line:
                print(line)


def read_stream():
    for line in streaming(['AAPL', 'GOOG']):
        print(line)


streaming(['AAPL', 'GOOG'])'''