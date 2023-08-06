from weeemake_pi import *

# Joystick Module
class WeJoystick:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):  # index: 0->X, 1->Y
    cmd='M13 '+str(self.port)+' 2 3\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 0:
          return (255-value[0])
        elif index == 1:
          return value[1]