from weeemake_pi import *

# Vibration Motor
class WeVibrationMotor:
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def run(self, speed):  # speed: 0~255
    cmd='M11 '+str(self.port)+' 3 1 '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)