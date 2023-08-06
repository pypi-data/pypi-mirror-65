from weeemake_pi import *

# RGB Strip
class WeRGBStrip:
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def showRGB(self,index,color):  # index: 0(All),1,2,3,4,5,...
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M6 '+str(self.port)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)