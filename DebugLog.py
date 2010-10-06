import logging
import os
import sys
import traceback
from datetime import datetime

HOME_OPERATING_SYSTEM = 'nt'
LOG_LEVEL = logging.ERROR
LOG_FILENAME = 'debugLog.txt'

class Log():
    def __init__(self):
        self.doNothing = False
        if os.name != HOME_OPERATING_SYSTEM:
            self.doNothing = True
        else:
            logging.basicConfig(filename = LOG_FILENAME, level = LOG_LEVEL)
            
            self.turnStartTime = datetime.now()
            self.turnNumber = 1
        
    def debug(self, s):
        if not self.doNothing:
            time = self.timeSinceTurnStart()
            logging.debug(time + ' : ' + s)
            
    def error(self, s):
        if not self.doNothing:
            time = self.timeSinceTurnStart()
            logging.error(time + ' : ' + s)
            
    def startTurn(self):
        if not self.doNothing:
            logging.debug('\n**Starting turn ' + str(self.turnNumber) + ' **\n\n')
            self.turnStartTime = datetime.now()
            self.turnNumber += 1
        
    def timeSinceTurnStart(self):
        timeDelta = (datetime.now() - self.turnStartTime)
        s = str(timeDelta.seconds)
        us = str(timeDelta.microseconds)
        time = s + '.' + '0' * (6-len(us)) + us
        
        return time
    
    def exc(self, e, s = None):
        if not self.doNothing:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
            time = self.timeSinceTurnStart()
            if s is None:
                logging.error(time + ' : EXCEPTION: ' + str(e))
            else:
                logging.error(time + ' : ' + s)
                
            logging.error('\n'.join(trace))
            
    def stop(self):
        """stop printing log messages"""
        self.doNothing = True
    def start(self):
        """start printing log messages"""
        self.doNothing = False

log = Log()