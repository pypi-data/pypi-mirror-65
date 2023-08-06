from weeemake_pi import *

#  LED Panel Module-Matrix 7*21
class WeLEDPanel_7_21: 
  def __init__(self, port):
    self.port = port    # port:PORT_*

  def showNumber(self, value):  # value: -999~9999
    cmd='M24 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
  
  def showString(self, x, y, string):
    cmd='M26 '+str(self.port)+' '+str(x)+' '+str(y)+' '+string+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def showBitmap(self, x, y, bitmap):
    cmd='M27 '+str(self.port)+' '+str(x)+' '+str(y)
    for i in range(0,21):
      cmd = cmd +' '+str(bitmap[i])
    cmd = cmd + '\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def turnOnDot(self, x, y):
    cmd='M21 '+str(self.port)+' '+str(x)+' '+str(y)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def turnOffDot(self, x, y):
    cmd='M22 '+str(self.port)+' '+str(x)+' '+str(y)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def clearScreen(self):
    cmd='M23 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)