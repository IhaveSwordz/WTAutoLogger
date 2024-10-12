import json
import os
import time
import datetime
import urllib.request

from src.Path import Path
from src.DataManager.DataCollectorManager import Main
from src.DataManager import DatabaseManager
from src.signals import Signals
from src.QThreader import Thread
from src.DebugLogger import Debug
from src.DataManager.ReplayReader import Lookup

'''
handle thread creation and error handling for DataCollectorManager.py
'''


class DataCollectorHandler:
    def __init__(self):
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
        Debug.logger.log("Handled", error)
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
        most_recent_file = None
        most_recent_time = 0

        # THIS CODE IS NOT MINE, used to get most recent replay in directory
        # iterate over the files in the directory using os.scandir
        for entry in os.scandir(Path.wrpl_path):
            if entry.is_file() and entry.name.endswith(".wrpl"):
                # get the modification time of the file using entry.stat().st_mtime_ns
                mod_time = entry.stat().st_mtime_ns
                if mod_time > most_recent_time:
                    # update the most recent file and its modification time
                    most_recent_file = entry.name
                    most_recent_time = mod_time

        lookup = Lookup(Path.wrpl_path + "/" + most_recent_file)
        lookup.lookup()
        js["hash"] = lookup.get_id()
        online_wl = js["winner"]
        file_wl = lookup.wl
        wl = None
        if online_wl != 0:
            wl = online_wl
        elif file_wl != 0 and file_wl is not None:
            wl = file_wl
        else:
            wl = 0
        # print(lookup.get_dict())

        player = lookup.get_dict()[lookup.owner_id.decode("utf-8")]
        if wl == 0:
            pass
        elif js["team1Tag"] == player["tag"]:
            pass
        elif js["team2Tag"] == player["tag"]:
            if wl == 1:
                wl = 2
            elif wl == 2:
                wl = 1
        else:
            wl = -1


        Debug.logger.log("SQL", f"Hash: {js["hash"]}")
        if self.db_manager.validate(js["hash"]):
            Debug.logger.log("SQL", "logging battle in db")
            self.db_manager.addLog(js, lookup.get_json())
        else:
            Debug.logger.log("SQL", "Tried to log battle already in db")
        # if js["hash"] in [log["hash"] for log in data["battles"]]:
        #     Debug.logger.log("SQL", "logfile aborted, similar hash found")
        #     return

        # Debug.logger.log("SQL", "logging battle in json file")
        # data["battles"].append(js)
        # with open(self.saveFile, "wb") as f:
        #     f.write(bytes(json.dumps(data).encode("utf-8")))
