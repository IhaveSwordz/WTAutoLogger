import json
import urllib.request
import urllib.error
import os
import time
import traceback

from src.Path import Path
from src.DataManager.DataCollector import Battle
from src.signals import Signals
from src.DataManager.converter import DataGet


from PySide6.QtCore import (QRunnable, Slot)

URL = "http://localhost:8111/hudmsg?lastEvt=0&lastDmg=0"
GameOnURL = "http://localhost:8111/map_info.json"
winLossURL = "http://localhost:8111/mission.json"
saveFile = "newFile.json"
# saveFile = "saveFile.json"
timeout = 1

'''
This class handles the overhead of actually running the data collecter. 

This has the chance to be heavily optimized 
because I rerun the collector script (DataCollector.py) each time there is new info because sometimes its goes wrong 
and I dont know why
TODO: figure out why I had to do all that

it is set as a QRunnable to allow for easu threading using QT
'''


class Main(QRunnable):
    @staticmethod
    def incoming(data: int):
        # print("INCOMING")
        # print(type(data))
        if data == 2:
            print("starting")
            Main.do_run = True
        elif data == 0:
            print("stopping")
            Main.do_run = False
        elif data == 5:
            print("exiting")
            Main.exit = True

    do_run = False
    exit = False

    Signals.signals.data.connect(incoming)
    def __init__(self, *args, **kwargs):
        super(Main, self).__init__()
        print("Starting Main")
        self.fn = self.mainLoop
        self.args = args

        self.kwargs = kwargs
        self.Battle = Battle()
        self.homeTeam = ["SADAF", "P1KE"]
        # success, fail, running
        self.state = ""
        self.errors = 3


        p = Path.path
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

    def updateBattle(self, logs):
        for log in logs:
            self.Battle.update(log)

    def log_file(self):
        print("logfile called")
        who = 0
        js = self.Battle.getJSON()

        # done to check which team won the battle

        t1t = js["team1Data"]["tag"]
        t2t = js["team2Data"]["tag"]
        if self.state == "success":
            if t1t in self.homeTeam:
                who = 1
            elif t2t in self.homeTeam:
                who = 2
        if self.state == "fail":
            if t1t in self.homeTeam:
                who = 2
            elif t2t in self.homeTeam:
                who = 1
        js.update({"winner": who})
        print(js)
        Signals.signals.sql.emit(js)
        self.Battle = Battle()


    @staticmethod
    def GetGameData():
        with urllib.request.urlopen(URL) as f:
            json_info = json.loads(f.read().decode('utf-8'))['damage'][::-1]
            data = [dat for dat in json_info if "_DISCONNECT_" not in dat['msg'] and "disconnected" not in dat['msg']]
            return data[:100]


    def getGameState(self):
        self.winLoss()
        with urllib.request.urlopen(GameOnURL) as f:
            dat = json.loads(f.read().decode('utf-8'))
            print(f"getGameState: {dat['valid']}, {self.state}")
            if self.state != "running" and self.state != "":
                return False
            elif self.state == "running":
                return True
            return dat['valid'] is not False


    def winLoss(self):
        with urllib.request.urlopen(winLossURL) as f:
            dat = json.loads(f.read().decode('utf-8'))
            self.state = dat["status"]

    def reset(self):
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

        out = self.get_data(data)
        if out == 1:
            self.log_file()
        else:
            print("error found when getting data to log")
        print("------------------------------------------------------")
        print("BATTLE END")
        print("------------------------------------------------------")

    def get_data(self, data):
        try:
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
            print(self.Battle)
            Signals.signals.logs.emit(self.Battle.getData())
            return 1
        except Exception as e:
            print("ERROR: ", e)
            Signals.signals.error.emit([e, traceback.format_exc()])
            return -1

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
                            print("BATTLE END TYPE 1")
                            gameInSession = False
                            count = timeout.__int__()
                            self.reset()
                            continue

                    # print("doing checkv")
                    self.winLoss()
                    '''
                    if recent - data[0]['time'] < 5:
                        recent = data[0]['time']
                    else:
                        print("BATTLE END TYPE 2")
                        gameInSession = False
                        recent = data[0]['time']
                        count = timeout.__int__()
                        self.reset()
                        continue
                    '''
                    prev = data[0]
                    updated = False
                    for i in data[1::]:
                        if i['time'] <= prev['time'] and i['msg'] not in collected:
                            collected.append(i['msg'])
                            prev = i
                            updated = True
                        else:
                            break
                    if updated:
                        self.Battle = Battle()
                        out = self.get_data(data)
                else:
                    # print(self.getGameState())
                    if self.getGameState():
                        gameInSession = True
            except urllib.error.URLError as e:
                Signals.signals.condition.emit(0)
                print("War thunder is not running")