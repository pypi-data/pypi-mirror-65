from weeemake_pi import *

# Adapter Module V2.0
class WeAdapter:
  """docstring for WeAdapter"""
  def __init__(self, port):
    self.port = port  # port:PORT_*

  def servo_write(self,slot,angle):  # slot:1~4  angle:0~180
    cmd='M81 '+str(self.port)+' '+str(slot)+' '+str(angle)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def rgb_show(self,slot,index,color):  # slot:1~4  index:0(All),1,2,3,...  color:#FFFFFF
    temp=color[1:7]
    aa=a2b_hex(temp)
    red=(aa[0])
    green=(aa[1])
    blue=(aa[2])
    cmd='M82 '+str(self.port)+' '+str(slot)+' '+str(index)+' '+str(red)+' '+str(green)+' '+str(blue)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def ds18b20_read(self,slot):
    cmd='M83 '+str(self.port)+' '+str(slot)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return round(eval(value),2)
  
  def digital_write(self,slot,value):  # slot:1~4  value:0/1
    cmd='M84 '+str(self.port)+' '+str(slot)+' '+str(vaule)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def digital_read(self,slot):
    cmd='M85 '+str(self.port)+' '+str(slot)+' 1\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

  def analog_read(self,slot):
    cmd='M86 '+str(self.port)+' '+str(slot)+' 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)