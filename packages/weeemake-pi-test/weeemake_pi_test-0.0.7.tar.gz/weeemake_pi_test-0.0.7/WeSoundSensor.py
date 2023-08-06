from weeemake_pi import *

# Sound Sensor
class WeSoundSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_2

  def getValue(self):
    cmd='M3 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)