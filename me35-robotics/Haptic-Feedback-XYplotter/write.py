#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Port
from pybricks.ev3devices import (Motor, TouchSensor,
ColorSensor, UltrasonicSensor, GyroSensor)
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import AnalogSensor, UARTDevice
import time
import random

ev32 = EV3Brick()

# Initializing the uart device
uart2 = UARTDevice(Port.S1, 9600, timeout=2000)

# Initializing all signals
motorx = Motor(Port.A)
motory = Motor(Port.B)
sensor = ColorSensor(Port.S2)

while True: 
    text =uart2.read_all()
    if text == b'R':
        motorx.run(500)
    elif text == b'L':
        motorx.run(-500)
    elif text == b'N':
        motorx.run(0)
    elif text == b'F':
        motory.run(500)
    elif text == b'B':
        motory.run(-500)
    elif text == b'M':
        motory.run(0)

    # Reading out the sensor data and writing it over UART
    if not (sensor.color()) == Color.WHITE):
        h = 'W'
    elif (sensor.color() == Color.WHITE):
        h = 'H'
        print(h)
        uart2.write(h)