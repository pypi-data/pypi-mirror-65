from weeemake_pi import *

# Stepper Motor
class WeStepperMotor:
  """docstring for WeStepperMotor"""
  def __init__(self, port):
    self.port = port  # port:PORT_1~PORT_4

  def run(self):
    cmd='M41 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def stop(self):
    cmd='M42 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def move(self, position):
    cmd='M43 '+str(self.port)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def moveTo(self, position):
    cmd='M44 '+str(self.port)+' '+str(position)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setPositionOrigin(self):
    cmd='M45 '+str(self.port)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setSpeed(self, speed):  # speed: 0~254
    cmd='M46 '+str(self.port)+' '+str(speed)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)

  def setMicroStep(self, value):  # value: 1,2,4,8,16,32
    cmd='M47 '+str(self.port)+' '+str(value)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)