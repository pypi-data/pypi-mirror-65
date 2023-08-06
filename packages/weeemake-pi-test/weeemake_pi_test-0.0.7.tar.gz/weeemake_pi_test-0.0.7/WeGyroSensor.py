from weeemake_pi import *

# Gyro Sensor
class WeGyroSensor:
  """docstring for GyroSensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
 
  def getValue(self, index):   # index: 0->AngleX, 1->AngleY, 2->AngleZ, 3->AccelerationX, 4->AccelerationY, 5->AccelerationZ
    cmd='M61 '+str(self.port)+' '+str(index)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    value=weSerial.readline()
    return eval(value)