from weeemake_pi import *

# Single LED Module
class WeSingleLED:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setLight(self, value):  # value: 0, 1
    cmd='M2 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)