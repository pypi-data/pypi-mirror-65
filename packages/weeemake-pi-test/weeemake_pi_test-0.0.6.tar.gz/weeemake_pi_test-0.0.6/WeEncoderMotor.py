from weeemake_pi import *

# Encoder Motor
class WeEncoderMotor:
  """docstring for WeEncoderMotor"""
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_4

  def run(self, speed):  # speed: -255~255
    cmd='M31 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def runSpeed(self, speed):  # speed: -255~255
    cmd='M32 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def move(self, speed, position):  # speed: -255~255
    cmd='M33 '+str(self.port)+' '+str(speed)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def moveTo(self, speed, position):  # speed: -255~255
    cmd='M34 '+str(self.port)+' '+str(speed)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setPositionOrigin(self):
    cmd='M35 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
  
  def getCurrentPosition(self):
    cmd='M36 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)

  def stop(self):
    cmd='M37 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)