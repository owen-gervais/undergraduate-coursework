#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import serial

# Data slicing functions to coordinate the IMU data from the Arduino Nano
# into python lists

def separateTerms (data, index):
     tempData = data[index]
     return tempData

def populateArrays (data,tempData):
     data.append(tempData)
     return data

def clearArrays ():
     data_x = []
     data_y = []


s=serial.Serial("/dev/ttyACM0",9600)

# Pre-initializing lists for later population
x_Accel = []
y_Accel = []
data_x = []
data_y = []

# Init
touch = TouchSensor(Port.S1)
timer = StopWatch()

# Initializing all of the arrays
while True:
     # Only activates if the signal is complete, tuning for the slower clock speed of the EV3
     data=s.read(s.inWaiting()).decode("utf-8")
     data = data.splitlines()

     #print('size = %d, buffer = %d' % (len(data),s.inWaiting()))

     if not len(data) == 0:
          imu = data[-1].split(',')
          if len(imu) == 7: 
               temp_yA = separateTerms(imu,1)
               temp_zA = separateTerms(imu,2) #
               deltaT = separateTerms(imu,6) #milliseconds


               print('IMU:', imu)
               print('deltaT: ', deltaT)
               print('tempy', temp_yA)
               print('tempz:', temp_zA)

               if deltaT != '':
                    velY = float(temp_yA)*float(deltaT)
                    velZ = float(temp_zA)*float(deltaT)

                    print('velY: ',velY)
                    print('velZ: ', velZ)
                    
# Tuning factors to determine the directions of the wand movement

                    if touch.pressed() == True:
                         if velZ > 3:
                              ev3.speaker.beep(393)
                              wait(200)
                         elif velZ < -1.5:
                              ev3.speaker.beep(436.7)
                              wait(200)
                         elif velY > 1:
                              ev3.speaker.beep(491.2)
                              wait(200)
                         elif velY < -2:
                              ev3.speaker.beep(524)
                              wait(200)
                    else: 
                         if velZ > 3:
                              ev3.speaker.beep(262)
                              wait(200)
                         elif velZ < -1:
                              ev3.speaker.beep(294.8)
                              wait(200)
                         elif velY > 1.5:
                              ev3.speaker.beep(327.5)
                              wait(200)
                         elif velY < -2:
                              ev3.speaker.beep(349.3)
                              wait(200)


          
              

                  

















              





              








          

               
