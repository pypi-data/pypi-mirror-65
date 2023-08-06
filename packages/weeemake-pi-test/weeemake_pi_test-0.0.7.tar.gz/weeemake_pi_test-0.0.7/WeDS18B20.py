from weeemake_pi import *

# DS18B20
class WeDS18B20:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def getValue(self):
    value=''
    cmd='M8 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)