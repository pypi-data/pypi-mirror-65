from weeemake_pi import *

# RGB Ultrasonic Sensor
class WeUltrasonicSensor:
  def __init__(self, port):
    self.port = port  # port:PORT_*
    self.RGB_data=[0,0,0,0,0,0]

  def distanceCM(self):
    cmd='M13 '+str(self.port)+' 2 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        distance = (value[1]<<8|value[0]) / 17.57
        if distance > 500:
          return 500
        else:
          return round(distance,2)

  def showRGB(self,index,color):   # index: 1->right, 2->left, 3->all
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M11 '+str(self.port)+' 3 6'
    if index & 1 != 0:
      self.RGB_data[0]=red
      self.RGB_data[1]=green
      self.RGB_data[2]=blue
    if index & 2 != 0:
      self.RGB_data[3]=red
      self.RGB_data[4]=green
      self.RGB_data[5]=blue
    if index & 3 != 0:
      for i in range(0,6):
        cmd = cmd + ' ' + str(self.RGB_data[i])
      cmd = cmd + '\r\n'
      weSerial.write(bytearray(cmd.encode('utf-8')))
      time.sleep(0.05)