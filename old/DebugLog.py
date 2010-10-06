"""
class newFile(file):
  def __init__(self, fileObject):
    self.fileObject = fileObject
  def write(self, s):
    self.fileObject.write(s + '\n')
    self.fileObject.flush()

from sys import stderr as log
from datetime import datetime
timeString = datetime.now().isoformat().replace('.', '_').replace(':', '_').replace('-', '_')
filename = 'debugLogs/log_%s.txt' % timeString
log = newFile(open(filename, 'w'))
log.write('created log object')
"""