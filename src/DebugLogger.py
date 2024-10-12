import datetime
import os
import time
import datetime
import random
from oslo_concurrency import lockutils

from src.Path import Path
from src.signals import Signals
from src.Path import Path

'''
this handles writing important info to files and debug menu
'''

PRINT_LOGS = True

class Logger:
    path = Path.path

    def __init__(self):
        self.start = time.time()
        self.file_path = None


    def enable_filing(self):
        self.file_path = self.path + "/src/Output/Logs"
        count = os.listdir(self.file_path)
        list_of_files = os.listdir(self.file_path)

        if len(list_of_files)-1 >= 20:

            full_path = [f"{self.file_path}/{x}" for x in list_of_files if x != ".txt"]
            oldest_file = min(full_path, key=os.path.getctime)
            os.remove(oldest_file)

        self.write_file = f"{datetime.datetime.now()}.log".replace(" ", "-").replace(":", "-")
        with open(f"{self.file_path}/{self.write_file}", "x") as f:
            pass

    # used to get relative time from start of module

    def get_time(self):
        return round(time.time() - self.start, 4)

    # writes text to log file as well as debug display
    @lockutils.synchronized('not_thread_process_safe', fair=True)
    def _write_text(self, text):
        with open(f"{self.file_path}/{self.write_file}", "a", encoding="utf-8") as f:
            f.write(text + "\n")
        Signals.signals.debug.emit(text)



    # given a caller (what kind of log it is) and a message it formats it and writes it
    def log(self, caller, message):
        front, back = str(self.get_time()).split(".")
        if self.file_path is not None:
            self._write_text(f"{front:>10}.{back:<4} | {caller:<20} | {str(message)}")
        if PRINT_LOGS:
            print(f"{front:>10}.{back:<4} | {caller:<20} | {str(message)}")

    # used to write special messages without a time count or caller
    def special_log(self, message):
        self._write_text(str(message))
        if PRINT_LOGS:
            print(message)


class Debug:
    logger = Logger()


if __name__ == "__main__":
    log = Debug.logger
    log.log("WOMP", "GET WOMP")
    time.sleep(random.random())
    log.log("GErmany", "Leopard")
    time.sleep(random.random())
    log.log("GErmany", "Leopard")
    time.sleep(random.random())
    log.log("GErmany", "Leopard")
    time.sleep(random.random())
    log.log("GErmany", "Leopard")
    time.sleep(random.random())
    log.log("GErmany", "Leopard")
    time.sleep(random.random())
    log.log("GErmany", "Leopard")
