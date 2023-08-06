from weeemake_pi import *

# Button On Board
class WeButton:
  def __init__(self, port):
    self.port = port  # port:OnBoard_Button

  def getValue(self):
    cmd='M1 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)