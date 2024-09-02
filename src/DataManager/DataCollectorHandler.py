import json
import time
import datetime
import urllib.request

from src.Path import Path
from src.DataManager.DataCollectorManager import Main
from src.DataManager import DatabaseManager
from src.signals import Signals
from src.QThreader import Thread

'''
handle thread creation and error handling for DataCollectorManager.py
'''


class DataCollectorHandler:
    def __init__(self):
        print("womp womp")
        self.saveFile = "src/Output/newFile.json"
        self.DBFile = "src/Output/Data.db"
        self.URL = "http://localhost:8111/hudmsg?lastEvt=0&lastDmg=0"
        self.path = Path.path
        Thread.use_thread(Main)

        Signals.signals.error.connect(self.error_handler)
        Signals.signals.sql.connect(self.sql_logging)
        self.db_manager = DatabaseManager.Manager()

    '''
    DataManager can call an error and this handles writing it disk
    
    '''

    def error_handler(self, error: list):
        print(error)
        self.errors = 0
        t = datetime.datetime.now(datetime.UTC)
        t = f"{t.year}-{t.month}-{t.day}-{t.hour}-{t.minute}-{t.second}"
        with urllib.request.urlopen(self.URL) as f:
            battle_data = json.loads(f.read().decode("utf-8"))
        with open(f"{self.path}/src/Output/ERROR-{t}.json", "x"):
            pass
        payload = {"battle": battle_data, "error": str(error)}
        with open(f"{self.path}/src/Output/ERROR-{t}.json", "wb") as f:
            f.write(bytes(json.dumps(payload).encode("utf-8")))

    def sql_logging(self, js):
        if not js['players']:
            print("logfile aborted, bad log")
            return
        if js["hash"] is None:
            print("logfile aborted, no Hash")
            return
        with open(self.saveFile, "rb") as f:
            data: dict = json.load(f)
        if self.db_manager.validate(js["hash"]):
            print("logging battle in db")
            self.db_manager.addLog(js)
        if js["hash"] in [log["hash"] for log in data["battles"]]:
            # print([log["hash"] for log in data["battles"]])
            print("logfile aborted, similar hash found")
            return
        print("logging battle in json file")
        data["battles"].append(js)
        with open(self.saveFile, "wb") as f:
            f.write(bytes(json.dumps(data).encode("utf-8")))
