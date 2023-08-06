from weeemake_pi import *

# 4-Digital LED Module
class We7SegmentDisplay:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def showNumber(self, value):  # value: -999~9999
    cmd='M71 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)