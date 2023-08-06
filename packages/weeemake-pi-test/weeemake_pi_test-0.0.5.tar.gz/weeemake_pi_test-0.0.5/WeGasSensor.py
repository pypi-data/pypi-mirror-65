from weeemake_pi import *

# Gas Sensor
class WeGasSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    cmd='M13 '+str(self.port)+' 2 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]