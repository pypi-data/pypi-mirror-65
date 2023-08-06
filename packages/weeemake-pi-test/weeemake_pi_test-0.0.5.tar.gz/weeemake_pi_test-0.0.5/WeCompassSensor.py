from weeemake_pi import *

# Compass Sensor
class WeCompassSensor:
  """docstring for WeCompassSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getValue(self, index):   # index: 0->X, 1->Y, 2->Z
    cmd='M51 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)