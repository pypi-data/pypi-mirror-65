from weeemake_pi import *

# Atomizer Module
class WeAtomizer:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setRun(self, value):  # value: 0, 1
    cmd = ''
    if value == 0:
      cmd='M11 '+str(self.port)+' 3 0\r\n'
    elif value == 1:
      cmd='M11 '+str(self.port)+' 2 0\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)