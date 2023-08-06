from weeemake_pi import *

# Servo
class WeServo:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def write(self, angle):   # angle: 0~180
    cmd='M5 '+str(self.port)+' '+str(angle)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)