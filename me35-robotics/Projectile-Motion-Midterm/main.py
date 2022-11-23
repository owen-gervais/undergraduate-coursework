#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import *
import ubinascii, ujson, urequests, utime

#---------------------------------------------------------------------------------
# FUNCTIONS: 

def RunAIModel(dist,baseMotor,baseMotor2):
# Input: dist (distance measured from ultrasonic sensor)
#
# Output: speed (motor drive speed)
#
# The below function makes use of the trained AI model using the obtained training
# data. The equation is derived from the linear regression of the dataset, which
# proved to be the best fit of the data

     speed = 1.2933*dist + 140.27
     RunMotors(speed,baseMotor,baseMotor2)
    

def RunPhysModel(dist,baseMotor,baseMotor2):
# Input: dist (distance measured from ultrasonic sensor)
#
# Output: speed (motor drive speed)
#
# The below function uses a Newtonian Physics model in order to obtain the 
# required motor speed to land in the cup

# Initializes all state variables for the model
     g = 9.81*1000
     R = 140 
     r = 51/2
     y0 = 140.20
     theta = pi/4

# Initializes a tuning factor for the model
     tuning = 1.1

# Runs the model correcting for the rotation speed and tuning
     phys = (1/(cos(theta)))*sqrt((.5*g*(dist**2))/(dist*tan(theta)+y0))
     speed = phys*(180/(pi*(R+r)))*tuning

     RunMotors(speed,baseMotor,baseMotor2)


def RunMotors(speed,baseMotor,baseMotor2):
# Input: speed (motor drive speed)
#        baseMotor (drive motor 1)
#        baseMotor2 (drive motor 2)

     rotation_angle = 500
     baseMotor.run_angle(speed, rotation_angle, Stop.COAST, False)
     baseMotor2.run_angle(speed, rotation_angle, Stop.COAST, True)


#---------------------------------------------------------------------------------
# SYSTEMLINK FUNCTIONS: 

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
          print(data)
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

#---------------------------------------------------------------------------------
# MAIN CODE: 

# API KEY
Key = 'nP2wSEqGl-xYpCbU4DPqXhE6oeRSpYPqExh1I8y_6d'

# Initializing ev3 Block
ev3 = EV3Brick()


# Initializing Swing Motor Instances
baseMotor = Motor(Port.C, Direction.CLOCKWISE)
baseMotor2 = Motor(Port.A, Direction.CLOCKWISE)


# Intializing Ultrasonic Sensor Instance
sense = UltrasonicSensor(Port.S2)
dist = sense.distance()


while True:
# GET call for the systemlink activation
     l_activate = Get_SL('launch_Activate')
     model = Get_SL('model_Select')

# Reads in the ultrasonic sensor data for each trial
     dist = sense.distance()

# Reads in model and actiavtion state 
     if (model == '1'):
          if (l_activate == '1'):
               
               print('Using AI')

# Runs the AI model in this case
               RunAIModel(dist,baseMotor,baseMotor2)

# Reads in model and activation state
     elif (model == '-1'):
          if (l_activate == '1'):

               print('Using Physics')

# Runs the Physics model in this case
               RunPhysModel(dist,baseMotor,baseMotor2)




