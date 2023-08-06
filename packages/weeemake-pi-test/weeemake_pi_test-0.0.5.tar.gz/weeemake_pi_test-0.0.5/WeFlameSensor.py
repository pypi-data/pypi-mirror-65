from weeemake_pi import *

# Flame Sensor
class WeFlameSensor:
  """docstring for WeFlameSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):   # index: 1->S1, 2->S2, 3->S3
    cmd='M13 '+str(self.port)+' 2 3\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return int(value[0])
        elif index == 2:
          return int(value[1])
        elif index == 3:
          return int(value[2])