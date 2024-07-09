import json
import urllib.request
from DataCollector import Battle
from converter import DataGet
import DatabaseManager
import os

URL = "http://localhost:8111/hudmsg?lastEvt=0&lastDmg=0"
GameOnURL = "http://localhost:8111/map_info.json"
winLossURL = "http://localhost:8111/mission.json"
saveFile = "newFile.json"
# saveFile = "saveFile.json"
timeout = 5


class Main:
    def __init__(self):
        self.Battle = Battle()
        self.dataGet = DataGet()
        self.db_manager = DatabaseManager.Manager()
        if not os.path.exists("newFile.json"):
            with open("newFile.json", "xb"):
                pass
            with open("newFile.json", "wb") as f:
                f.write(b"{\"battles\" : []}")
                print("created json storage file")
        else:
            print("found newFile.json")

    def updateBattle(self, logs):
        for log in logs:
            self.Battle.update(log)

    def logFile(self):
        print("logfile called")
        js = self.Battle.getJSON()
        if not js['players']:
            print("logfile aborted, bad log")
            return
        if js["hash"] is None:
            print("logfile aborted, no Hash")
            return
        with open(saveFile, "rb") as f:
            data: dict = json.load(f)
        if self.db_manager.validate(js["hash"]):
            self.db_manager.addLog(js)
        if js["hash"] in [log["hash"] for log in data["battles"]]:
            # print([log["hash"] for log in data["battles"]])
            print("logfile aborted, similar hash found")
            return
        data["battles"].append(js)
        with open(saveFile, "wb") as f:
            f.write(bytes(json.dumps(data).encode("utf-8")))
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
        self.logFile()
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

    def mainLoop(self):
        recent = 0
        gameInSession = True
        count = timeout.__int__()
        collected = []
        while True:
            if gameInSession:
                data = self.GetGameData()
                # print(self.Battle.getJSON())
                if not self.getGameState():
                    print(count)
                    if count > 0:
                        count -= 1
                    else:
                        gameInSession = False
                        count = timeout.__int__()
                        self.reset()
                        continue
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


b = Main()
b.mainLoop()
# print(len(stuff))
# print(stuff)