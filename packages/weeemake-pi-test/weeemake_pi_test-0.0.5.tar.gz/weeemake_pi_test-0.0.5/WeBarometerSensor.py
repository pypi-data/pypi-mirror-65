from weeemake_pi import *

# Barometer Sensor
class WeBarometerSensor:
  """docstring for WeBarometerSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def getPressure(self):
    cmd='M13 '+str(self.port)+' 3 4\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return round((value[0]|value[1]<<8|value[2]<<16|value[3]|24)/100,2)