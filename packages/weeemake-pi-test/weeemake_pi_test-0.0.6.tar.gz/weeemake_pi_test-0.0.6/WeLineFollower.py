from weeemake_pi import *

# Line Follower Sensor
class WeLineFollower:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self, index):   # index: 1->S1, 2->S2
    cmd='M13 '+str(self.port)+' 2 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        if index == 1:
          return int(number_map(value[0],0,255,1023,0))
        elif index == 2:
          return int(number_map(value[1],0,255,1023,0))