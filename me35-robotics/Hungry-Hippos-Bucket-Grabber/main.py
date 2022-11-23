#! /usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# importing SystemLink
import ubinascii, ujson, urequests, utime

import passwords

Key = key

def SL_setup():
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    headers = {"Accept":"application/json", "x-ni-api-key":Key}
    return urlBase, headers

def Put_SL(Tag, Type, Value):
    urlBase, headers = SL_setup()
    urlValue = urlBase + Tag + "/values/current"
    propValue = {"value":{"type":Type, "value":Value}}
    try:
        reply = urequests.put(urlValue,headers=headers. json=propValue).text        
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
        reply = 'failed'
    return reply

def Create_SL(Tag, Type):
    urlBase, headers = SL_setup()
    urlValue = urlBase + Tag
    propName={"type":Type,"path":Tag}
    try:
        urequests.put(urlTag,headers=headers,json=propName).text
    except Exception as e:
        print(e)


# We utilize the Joke REST API in order to write a Get_Joke fuction to generate
# random jokes
def Get_Joke():
    try:
        value = urequests.get("http://api.icndb.com/jokes/random").text
        data = ujson.loads(value)
        result = data.get("value").get("joke")
    except Exception as e:
        print(e)
        reply = 'failed'
    return result


# Creating an instancee of the Get_Joke() for pushing to Systemlink dashboard
jokeApi = Get_Joke()

# Creates the Joke Tag and pushes to the dashboard
Create_SL('Joke','STRING')
Put_SL('Joke','STRING',jokeApi)

# Assigning Motor variables and positions
right_motor = Motor(Port.A, Direction.CLOCKWISE)
left_motor = Motor(Port.B, Direction.CLOCKWISE)
bucket_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)

# Creates the tags on each instance in case the tags fot deleted
Create_SL('Right Motor', 'STRING')
Create_SL('Left Motor', 'STRING')
Create_SL('Bucket Motor', 'STRING')

# Initializes all motor values to zero for te start of the program
Put_SL('Right Motor','STRING','0')
Put_SL('Left Motor','STRING','0')
Put_SL('Bucket Motor','STRING','0')



while True:
    # GET call for each motor valye to grab te values inputted by the user in
    # Systemlink dashboard
    rightSpeed = Get_SL('Right Motor')
    leftSpeed = Get_SL('Left Motor')
    bucketPosition = Get_SL('Bucket Motor')

    # Runs the motors at the slider values on the Systemlink dashboard
    left_motor.run(-7*float(leftSpeed))
    right_motor.run(-7*float(leftSpeed))

    # Fire Bucket Control Condition
    if (bucketPosition == '1'):
        bucket_motor.run_time(-700*float(bucketPosition),800)
    elif (bucketPosition == '-1'):
        bucket_motor.run_time(700*float(1),800)
        

