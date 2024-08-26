import json
import urllib.request
import urllib.error
import os
import sys
import time
import traceback

from src.DataManager.DataCollector import Battle
from src.signals import Signals
from src.DataManager.converter import DataGet


from PySide6.QtCore import (QRunnable, Slot)

URL = "http://localhost:8111/hudmsg?lastEvt=0&lastDmg=0"
GameOnURL = "http://localhost:8111/map_info.json"
winLossURL = "http://localhost:8111/mission.json"
saveFile = "newFile.json"
# saveFile = "saveFile.json"
timeout = 5

'''
This class handles the overhead of actually running the data collecter. 

This has the chance to be heavily optimized 
because I rerun the collector script (DataCollector.py) each time there is new info because sometimes its goes wrong 
and I dont know why
TODO: figure out why I had to do all that

it is set as a QRunnable to allow for easu threading using QT
'''


class Main(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__()
        print("Starting Main")
        self.fn = self.mainLoop
        self.args = args
        self.kwargs = kwargs
        self.Battle = Battle()
        Signals.signals.data.connect(self.incoming)

        self.do_run = False
        self.exit = False
        p = os.environ["PYTHONPATH"]
        if not os.path.exists(f"{p}/src/Output/newFile.json"):
            with open(f"{p}/src/Output/newFile.json", "xb"):
                pass
            with open(f"{p}/src/Output/newFile.json", "wb") as f:
                f.write(b"{\"battles\" : []}")
                print("created json storage file")
        else:
            print("found newFile.json")

    @Slot()
    def run(self):
        print("running")
        self.fn()
        # self.fn(*self.args, **self.kwargs)

    def incoming(self, data: int):
        # print("INCOMING")
        # print(type(data))
        if data == 2:
            print("starting")
            self.do_run = True
        elif data == 0:
            print("stopping")
            self.do_run = False
        elif data == 5:
            print("exiting")
            self.exit = True
            # print("self.exit", self.exit)
        # print(data)

    def updateBattle(self, logs):
        for log in logs:
            self.Battle.update(log)

    def log_file(self):
        print("logfile called")
        js = self.Battle.getJSON()
        Signals.signals.sql.emit(js)
        self.Battle = Battle()

    @staticmethod
    def GetGameData():
        with urllib.request.urlopen(URL) as f:
            json_info = json.loads(f.read().decode('utf-8'))['damage'][::-1]
            data = [dat for dat in json_info if "_DISCONNECT_" not in dat['msg'] and "disconnected" not in dat['msg']]
            return data[:100]

    @staticmethod
    def getGameState():
        with urllib.request.urlopen(GameOnURL) as f:
            dat = json.loads(f.read().decode('utf-8'))
            # print(dat['valid'])
            return dat['valid'] is not False

    def reset(self):
        # print("reset: ", self.Battle.getJSON())
        self.Battle = Battle()
        data = self.GetGameData()
        collected = []
        prev = data[0]
        updated = False
        for i in data[1::]:
            if i['time'] <= prev['time'] and i['msg'] not in collected:
                collected.append(i['msg'])
                prev = i
                updated = True
            else:
                break

        self.getData(data)



        self.log_file()
        print("------------------------------------------------------")
        print("BATTLE END")
        print("------------------------------------------------------")

    def getData(self, data):
        prev = data[0]
        payload = []
        for i in data[1::]:
            if i['time'] <= prev['time']:
                prev = i
                payload.append(i)
            else:
                break

        for i in payload[::-1]:
            self.Battle.update(i)
        # print("getData: ", self.Battle.getJSON())
        print(self.Battle)
        Signals.signals.logs.emit(self.Battle.getData())

    def mainLoop(self):
        print("started main")
        recent = 0
        gameInSession = True
        count = timeout.__int__()
        collected = []
        while not self.exit:
            if not self.do_run:
                time.sleep(1)
                continue
            try:
                if gameInSession:
                    data = self.GetGameData()
                    if not self.getGameState():
                        print(count)
                        if count > 0:
                            count -= 1
                        else:
                            gameInSession = False
                            count = timeout.__int__()
                            self.reset()
                            continue
                    print("doing checkv")
                    if recent <= data[0]['time']:
                        recent = data[0]['time']
                    else:

                        gameInSession = False
                        recent = data[0]['time']
                        count = timeout.__int__()
                        self.reset()
                        continue

                    prev = data[0]
                    updated = False
                    for i in data[1::]:
                        if i['time'] <= prev['time'] and i['msg'] not in collected:
                            collected.append(i['msg'])
                            prev = i
                            updated = True
                        else:
                            break
                    #
                    if updated:
                        self.Battle = Battle()
                        self.getData(data)
                else:
                    if Main.getGameState():
                        gameInSession = True
            except urllib.error.URLError as e:
                Signals.signals.condition.emit(0)
                print("War thunder is not running")
            except Exception as e:
                print("ERROR: ", e)
                Signals.signals.error.emit([e, traceback.format_exc()])
                self.exit = True

