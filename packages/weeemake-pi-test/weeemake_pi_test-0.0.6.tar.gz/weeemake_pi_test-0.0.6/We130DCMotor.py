from weeemake_pi import *

# 130 DC Motor Module
class We130DCMotor:
  def __init__(self, port):
    self.port = port     # port:PORT_*

  def run(self,speed):  # speed: -255~255
    speed = max(-255, min(255, speed))
    if speed >= 0 :
      speed = (int)(speed/2.55)
    else:
      speed = (int)(100-speed/2.55)

    cmd='M11 '+str(self.port)+' 2 1 '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)