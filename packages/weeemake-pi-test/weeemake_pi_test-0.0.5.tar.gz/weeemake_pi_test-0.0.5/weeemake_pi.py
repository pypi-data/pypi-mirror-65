# -*- coding: utf-8 -*-
import serial
import time
from binascii import a2b_hex

weSerial=serial.Serial("/dev/ttyS0",9600,timeout=10)

PORT_A = 4
PORT_B = 5
PORT_C = 6
PORT_D = 9
PORT_1 = 14
PORT_2 = 15
PORT_3 = 2
PORT_4 = 3

OnBoard_Button = 21

M1 = 1
M2 = 2
M3 = 3
M4 = 4
M5 = 5
M6 = 6
M7 = 7
M8 = 8

def colour_rgb(r, g, b):
  r = round(min(100, max(0, r)) * 2.55)
  g = round(min(100, max(0, g)) * 2.55)
  b = round(min(100, max(0, b)) * 2.55)
  return '#%02x%02x%02x' % (r, g, b)

def number_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

from WeSoundSensor import *
from WeLightSensor import *

from WeButton import *

from WeDCMotor import *
from WeEncoderMotor import *
from WeStepperMotor import *
from WeServo import *
from We130DCMotor import *
from WeRelay import *
from WeAtomizer import *
from WeVibrationMotor import *

from WeJoystick import *
from We4LEDButton import *
from WePotentiometer import *

from WeRGB5Module import *
from WeRGBStrip import *
from WeSingleLED import *
from We7SegmentDisplay import *
from WeLEDPanel_7_21 import *

from WeHumiture import *
from WeGasSensor import *
from WeUltrasonicSensor import *
from WeSingleLineFollower import *
from WeLineFollower import *
from WeDS18B20 import *
from WePIRSensor import *
from WeTouchSensor import *
from WeFunnyTouchSensor import *
from WeColorSensor import *
from WeFlameSensor import *
from WeGestureSensor import *
from WePM25Sensor import *
from WeTiltSwitch import *
from WeUVSensor import *
from WeWaterSensor import *
from WeBarometerSensor import *
from WeCompassSensor import *
from WeGyroSensor import *

from WeAdapter import *
