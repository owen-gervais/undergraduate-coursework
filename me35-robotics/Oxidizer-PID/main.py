#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                    InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, 
                                    Soundfile, ImageFile, Allign)
from pybricks.tools import print, wait, Stopwatch
from pybricks.robotics import DriveBase

from pybricks.ev3devio import Ev3devSensor
import utime
import ev3dev2
import ev3dev2.port import LegoPort

class MySensor(Ev3devSensor): #Define Class
    _ev3dev_driver_name="ev3-analog-01"
    def readvalue(self):
        self._mode('ANALOG')
        return self._value(0)

def main():
    brick.sound.beep()
    sens1 = LegoPort(address = 'ev3-port:in1')
    sens1.mode = 'ev3-analog'
    utime.sleep(0.5)
    sensor_right = MySensor(Port.S1)
    sensor_left = MySensor(Port.S4)
    motor_right = Motor(Port.A)
    motor_left = Motor(Port.D)

    targetleft = 530
    targetright = 250
    KP = 3.75
    KD = .3
    KI = 0
    left_prev_error = 0
    right_prev_error = 0
    left_sum_error = 0
    right_sum_error = 0
    leftspeed = 0
    rightspeed = 0

    while not Button.CENTER in brick.buttons():
        print('left:')
        print(sensor_left.readvalue())
        print('right:')
        print(sensor_right.readvalue())

        #PID controller
        errorleft = sensor_left.readvalue() - targetleft
        print('left error:' + str(errorleft))
        errorright = sensor_right.readvalue() - targetright 
        print('right error:' str(errorright))

        leftspeed = (errorleft * KP) + ((errorleft - left_prev_error) * KD) + (left_sum_error * KI) + 375
        rightspeed = (errorright * KP) + ((errorright - right_prev_error) * KD) + (right_sum_error * KI) + 375
        
        left_prev_error = errorleft
        right_prev_error = errorright

        left_sum_error += errorleft
        right_sum_error += errorright

        motor_left.run(leftspeed)
        motor_right.run(rightspeed)


main()