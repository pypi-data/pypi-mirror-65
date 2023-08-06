from weeemake_pi import *

# Temperature and Humidity Sensor
class WeHumiture:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):  # index: 0->temperature, 1->humidity
    cmd='M13 '+str(self.port)+' 2 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return value[0]
        elif index == 0:
          return value[1]