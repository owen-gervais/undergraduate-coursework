#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Port
from pybricks.ev3devices import (Motor, TouchSensor,
ColorSensor, UltrasonicSensor, GyroSensor)
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import AnalogSensor, UARTDevice
import time
import random

ev3 = EV3Brick()

# Initializing the uart device
uart = UARTDevice(Port.S1, 9600, timeout=2000)

# Initializing the motors
motor1 = Motor(Port.A)
motor2 = Motor(Port.B)
motor3 = Motor(Port.C)

# Zeroing the initial angles
motor1.reset_angle(0)
motor2.reset_angle(0)

# Starting a timer
startTime = time.time()
timenow = time.time()

while True: 
    # Reads in the angles of motor 1 and 2 '
    yangle = -motor2.angle()
    xangle = motor1.angle()

    # Uses the Read positions to drive the system
    print('x=', xangle)
    print('y=', yangle)
    if xangle > 18:
        x = 'R'
    elif xangle < -18:
        x = 'L'
    else:
        x = 'N'
    if yangle > 18:
        y = 'F'
    elif yangle < -18:
        y = 'B'
    else:
        y = 'M'

    # Writes the signal
    uart.write(x)
    uart.write(y)
    fback = uart.read_all()

    # Runs the system
    if fback == b'W':
        motor3.run(1000)
        wait(0.01)
    elif fback == b'H':
        motor3.run(0)
        wait(.01)
