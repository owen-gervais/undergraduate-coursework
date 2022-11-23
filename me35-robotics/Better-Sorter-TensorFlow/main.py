#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()



import ubinascii, ujson, urequests, utime
     
password = open('passwords.txt')
Key = password.readline()
     
def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          #print(data)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result
     
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)

def RunMotor(angle,i_angle):   

     arm.run_target(100, angle)
     wait(50)
     carrier.run_angle(100, -180)
     wait(50)
     carrier.run_angle(-100, -180)
     arm.run_target(100, 0)

def isLongBoi():
    angle = 120
    i_angle = 180 
    RunMotor(angle,i_angle)

def isShortBoi():
     angle = 170
     i_angle = 180
     RunMotor(angle,i_angle)

def isVBoi():
     angle = 220
     i_angle = 180
     RunMotor(angle,i_angle)

def isLBoi():
     angle = 270
     i_angle = 180
     RunMotor(angle,i_angle)

def isGearBoi():
     angle = 320
     i_angle = 180
     RunMotor(angle,i_angle)

def isTriangleBoi():
     angle = 370
     i_angle = 180
     RunMotor(angle,i_angle)


arm = Motor(Port.A)
carrier = Motor(Port.B)
button = TouchSensor(Port.S1)
watch = StopWatch()

isTriangleBoi()
#isShortBoi()
while True:
     case = Get_SL('model_Select')
     if button.pressed() == True:

          if case == 'Long Boi':
               isLongBoi()
          elif case == 'Short Boi':
               isShortBoi()
          elif case == 'V Boi':
               isVBoi()
          elif case == 'L Boi':
               isLBoi()
          elif case == 'Gear Boi':
               isGearBoi()
          elif case == 'Triangle Boi':
               isTriangleBoi()
q






