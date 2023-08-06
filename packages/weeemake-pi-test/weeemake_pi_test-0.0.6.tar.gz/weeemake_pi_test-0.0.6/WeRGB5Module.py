from weeemake_pi import *

# RGB LED-5 Module
class WeRGB5Module:
  def __init__(self, port):
    self.port = port  # port:PORT_*
    self.RGB_data=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  def showRGB(self,index,color):  # index: 0(All),1,2,3,4,5
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M11 '+str(self.port)+' 2 15'
    if index == 0:
      for i in range(0,5):
        index = i * 3
        self.RGB_data[index] = green
        self.RGB_data[index + 1] = red
        self.RGB_data[index + 2] = blue
    elif(index <= 5):
      index = (index - 1) * 3
      self.RGB_data[index] = green
      self.RGB_data[index + 1] = red
      self.RGB_data[index + 2] = blue

    for i in range(0,15):
      cmd = cmd + ' ' + str(self.RGB_data[i])
    cmd = cmd + '\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)