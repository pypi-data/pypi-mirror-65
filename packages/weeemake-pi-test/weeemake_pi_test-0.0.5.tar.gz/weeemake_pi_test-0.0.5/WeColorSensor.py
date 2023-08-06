from weeemake_pi import *

# Color Sensor
class WeColorSensor:
  """docstring for WeColorSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def setLight(self, isOn):
    cmd='M11 '+str(self.port)+' 3 1 '+str(isOn)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def whitebalance(self):
    cmd='M11 '+str(self.port)+' 4 0\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def getValue(self, index):   # index: 1->red, 2->green, 3->blue, 4->light 
    cmd='M13 '+str(self.port)+' 2 8\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return int(value[1]<<8|value[0])
        elif index == 2:
          return int(value[3]<<8|value[2])
        elif index == 3:
          return int(value[5]<<8|value[4])
        elif index == 4:
          return int(value[7]<<8|value[6])