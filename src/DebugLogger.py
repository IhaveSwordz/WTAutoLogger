import datetime
import time

'''
this handles writing important info to files and debug menu
'''
class Logger_u:
    def __init__(self):
        self.start = time.time()
    # gonna be used to get relative time
    def get_time(self):
        return time.time() - self.start


l = Logger()
