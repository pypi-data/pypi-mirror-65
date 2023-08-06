from weeemake_pi import *

# PM2.5 Sensor
class WePM25Sensor:
  """docstring for WePM25Sensor"""
  def __init__(self, port):
    self.port = port  # port:PORT_*
  
  def setFanLaser(self, isOn):
    cmd='M11 '+str(self.port)+' 2 1 '+str(isOn)+'\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.01)

  def readPm1_0Concentration(self):
    cmd='M13 '+str(self.port)+' 3 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def readPm2_5Concentration(self):
    cmd='M13 '+str(self.port)+' 4 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def readPm10Concentration(self):
    cmd='M13 '+str(self.port)+' 5 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read0_3NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 6 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read0_5NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 7 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read1_0NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 8 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read2_5NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 9 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])

  def read5_0NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 10 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])
  
  def read10NumIn100ml(self):
    cmd='M13 '+str(self.port)+' 11 2\r\n'
    weSerial.write(bytearray(cmd.encode('utf-8')))
    time.sleep(0.05)
    count = weSerial.inWaiting() 
    if count > 0:
      value=weSerial.read(count)
      if len(value) == count:
        return int(value[0]<<8|value[1])