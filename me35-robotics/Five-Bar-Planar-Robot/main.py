#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from math import (acos, atan, sqrt, pi)
import ubinascii, ujson, urequests, utime
import random

# --------------------------- User Defined Functions -------------------------------

# User Defined toDegree function for conversions for the inverse kinematics
def toDegree(val):
# Input: a radian angle
# Output: an angle in degrees
    val = val * (180/pi)
    return val



def calcIK_angles(x_Tar,y_Tar):
# Input: The x and y positional inputs to robot arm
# Output: Uses the inverse kinematics formulas and returns the two motor angles

     PA_1 = sqrt((x_Tar + r_3)**2 + y_Tar**2)
     PA_2 = sqrt((x_Tar - r_3)**2 + y_Tar**2)

     theta_11 = acos(((PA_1)**2 + r_1**2 - r_2**2)/(2*r_1*PA_1))
     theta_12 = acos((x_Tar +r_3)/PA_1)

     theta_21 = acos(((PA_2)**2 + r_1**2 - r_2**2)/(2*r_1*PA_2))
     theta_22 = acos((x_Tar -r_3)/PA_2)

     theta_1 = theta_11 + theta_12
     theta_2 = theta_21 - theta_22

     return theta_1, theta_2



def runIK_TEST(theta_1, theta_2):
# Input: Theta_1 and Theta_2 
# Output: Printed Test Outputs for the IK

     print('-------------Drive Motor Angles-------------')
     print('theta_A1 :::', 135 - toDegree(theta_1),'Degrees')
     print('theta_A2 :::', toDegree(theta_2)-45, 'Degrees')
     print('---------------Test Concluded---------------')



def driveSystem(theta_1, theta_2):
# Input: Theta_1 and Theta_2
# Output: The system 

     lM.run_target(600, -1*(135 - toDegree(theta_1)),Stop.BRAKE, False)
     rM.run_target(600, toDegree(theta_2)+45, Stop.BRAKE, True)



def systemHome():
# The below code brings the robot to its zero state, accounts for the error
# in the return of the ev3 motors

     lM.run_target(150, 5,Stop.BRAKE, False)
     rM.run_target(150, 5, Stop.BRAKE, True)



def grabLaneValue(RNG):
# Input: RNG, random number generated
# Output: Positions of the output lanes based on the RNG inputted
     if RNG == 1:
          x_pos = -80
          y_pos = 95
     elif RNG == 2:
          x_pos = -80
          y_pos = 130
     elif RNG == 3: 
          x_pos = -80
          y_pos = 150
     else:
          x_pos = -80
          y_pos = 164
     return x_pos, y_pos

 

# -------------------------- SystemLink App-Key ----------------------------------
# classkey: bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0      
# personalkey: zpJ4VYEeaRsGM016V2EtWdH5IHSol0qB-O_YoqkTWW

#Key = 'zpJ4VYEeaRsGM016V2EtWdH5IHSol0qB-O_YoqkTWW'

# --------------------- SystemLink Operation Functions ---------------------------

# Sets up the initial urL for grabbing the tag in Systemlink
def SL_setup(Key):
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     #print('Got URL and Headers')
     return urlBase, headers
     


# Puts the Systemlink tag to SystemLink supplied
def Put_SL(Tag, Type, Value,place):
    if place =='home':
        key = 'zpJ4VYEeaRsGM016V2EtWdH5IHSol0qB-O_YoqkTWW'
    else: 
        key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
    urlBase, headers = SL_setup(key)
    urlValue = urlBase + Tag + "/values/current"
    propValue = {"value":{"type":Type,"value":Value}}
    try:
        reply = urequests.put(urlValue,headers=headers,json=propValue).text
    except Exception as e:
        print(e)         
        reply = 'failed'
    return reply



# Gets the Systemlink tag designated from Systemlink Cloud
def Get_SL(Tag,place):
    if place =='home':
        key = 'zpJ4VYEeaRsGM016V2EtWdH5IHSol0qB-O_YoqkTWW'
    else: 
        key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
    urlBase, headers = SL_setup(key)
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
     


# Creates the SL Tag at the designated App-Key
def Create_SL(Tag, Type,place):
    if place =='home':
        key = 'zpJ4VYEeaRsGM016V2EtWdH5IHSol0qB-O_YoqkTWW'
    else: 
        key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
    urlBase, headers = SL_setup(key)
    urlTag = urlBase + Tag
    propName={"type":Type,"path":Tag}
    try:
        urequests.put(urlTag,headers=headers,json=propName).text
    except Exception as e:
        print(e)



# -----------------------------------------------------------------------------
# Everything below in this section is main operating code for the robot and the 
# operation of the conveyor and output sensors. 
# -----------------------------------------------------------------------------



# --------------------------------- Main Section ------------------------------

# Initializing ev3 brick instance
ev3 = EV3Brick()



# Initializing the Motors and Sensors for the System
lM = Motor(Port.A)
rM = Motor(Port.B)
launchMotor = Motor(Port.C)
strtButton = TouchSensor(Port.S4)
conveyorMotor = Motor(Port.D)



# Zeroing all drive motor angles to zero
lM.reset_angle(0)
rM.reset_angle(0)



# Five Bar Robot - constants made global to limit arguments to user defined functions
r_1 = 86 # Length of first linkage (mm)
r_2 = 119 # Length of second linkage (mm)
r_3 = r_2/10 # Distance between drive motors 



# -----------------------------Initial Positions for Tuning-----------------------
# Button Drive - this is a starting position for drive
# x_positions, [-105]
# y_positions, [0]

# Conveyor Drive - this is a starting position for drive
# x_position, [160]
# y_position, [89]

# Initial Swinging Drive - this is a starting position for drive (outdated)
# x_position, [-175,175,-175,175,-170,170,-165,165,-160,160,-145,145,-135,135,-115,115,-90,90,-70,70,0]#[-170,-135, 0, 135,145, -135, 135]
# y_position, [0,0,20,20,40,40,60,60,80,80,100,100,120,120,140,140,160,160,170,170,175,175,179]#[20,120, 189, 120, 50, 20, 20 ]
# --------------------------------------------------------------------------------



# Drive Postiions
x_pos =[-105,160]
y_pos =[0,89]



# -----------------------------------------------------------------------------------
# This main loop runs through constantly checking the state of the system
# it only runs if the system is in the true state
# -----------------------------------------------------------------------------------

while True:

     # Pulling the state of START21 tag from Systemlink
     START21 = Get_SL('Start21','school')


     if START21 == 'true':
        # All x and y positions are relative to the Oxy corridinates
        theta_1, theta_2 = calcIK_angles(x_pos[0],y_pos[0])
        # Drive robot to target
        driveSystem(theta_1,theta_2)
        wait(500)
            

        if strtButton.pressed() == True:

            # Generates a Random Lane for Ball Deposit and shifts the
            # conveyor position to trigger the TensorFlow Model to run
            # on second computer.
            RNG = 3
            conveyorMotor.run_time(-150, 600, Stop.BRAKE, True)
            Put_SL('RunTensor','STRING','true','home')
                                                                                                                                                                                                                                                                                                                                                                
    
            # Homes the Robot
            systemHome()


            # Pause loop that waits for an update tag from Systemlink to
            # proceed with the operation.
            # Also resets all tags so that the process can be continuously
            # run. 
            while Get_SL('update','home') != 'true':
                    print('waiting for response......')
            Put_SL('update','STRING','false','home')
            Put_SL('RunTensor','STRING','false','home')  
            

            # If a ball was determined from the Tensorflow model the process
            # continues. 
            if Get_SL('runCLAW','home') == 'true':

                # Resets the runCLAW tag and Robot declares that it has found
                # a ball
                Put_SL('runCLAW','STRING','false','home') 
                ev3.speaker.say('Ball Detected')
                

                # Drives the system to conveyor, loads the ball into the claw,
                # and closes the claw to lock the ball into place
                theta_1, theta_2 = calcIK_angles(x_pos[1],y_pos[1])
                driveSystem(theta_1,theta_2)
                wait(500)
                conveyorMotor.run_time(-150, 625, Stop.BRAKE, True)
                launchMotor.run_target(300,140,Stop.BRAKE,True)
  

                # Grabs the randomly generated number and moves to the numbered
                # deposit lane, and drops the ball
                x_RNG, y_RNG = grabLaneValue(RNG)
                theta_1, theta_2 = calcIK_angles(x_RNG,y_RNG)
                driveSystem(theta_1,theta_2)
                launchMotor.run_target(300,0,Stop.BRAKE,True)


                # Switch next operating tag to true
                Put_SL('Start22','BOOLEAN','true','school')


        # Final system homing to end operation loop      
        systemHome()
        
