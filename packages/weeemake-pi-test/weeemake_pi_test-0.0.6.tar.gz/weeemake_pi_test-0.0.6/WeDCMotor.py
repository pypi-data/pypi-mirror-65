from weeemake_pi import *

# DC Motor
class WeDCMotor:
  def __init__(self, port):
    self.port = port  # port:M*
    self.dc_slot = [[None,None],[PORT_1,1], [PORT_1,2], [PORT_2,1], [PORT_2,2], [PORT_3,1], [PORT_3,2],[PORT_4,1], [PORT_4,2]]

  def run(self,speed):  # speed: -255~255
    speed = max(-255, min(255, speed))
    if speed >= 0 :
      speed = (int)(speed/2.55)
    else:
      speed = (int)(100-speed/2.55)

    cmd='M11 '+str(self.dc_slot[self.port][0])+' 2 2 '+str(self.dc_slot[self.port][1])+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)