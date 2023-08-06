from weeemake_pi import *

# Relay Module
class WeRelay:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def setNC(self, value):  # value: 0, 1
    cmd='M11 '+str(self.port)+' 2 1 '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)