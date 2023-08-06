from weeemake_pi import *

# UV Sensor
class WeUVSensor:
  """docstring for WeUVSensor"""
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
  
  def getIndex(self):
    cmd='M13 '+str(self.port)+' 3 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return value[0]