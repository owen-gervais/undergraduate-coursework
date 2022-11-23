# Import necessary Python libraries
# OpenCV library
import cv2
# Import library to plot histograms
import matplotlib.pyplot as plt 
# Python Imaging Library used to load images from files, and to create new images
import PIL.Image
# BytesIO implements read and write bytes data in memory
from io import BytesIO
# Library rto display stuff and clear stuff on Jupyter Notebook
import IPython.display
from IPython.display import clear_output
import numpy as np
# library that makes calls to openCv a bit more convenient
import imutils
# Library that alloss for serial communication
import serial

# Function that  converts array data to image
def array_to_image(a, fmt='jpeg'):
    # Create binary stream object
    f = BytesIO()

    # Convert array to binary stream object
    PIL.Image.fromarray(a).save(f, fmt)

    return IPython.display.Image(data=f.getvalue())


# Function to read the frame from camera
def get_frame(cam):
    # Capture frame-by-frame
    ret, frame = cam.read()
    # flip image for natural viewing
    frame = cv2.flip(frame, 1)
    return frame

# Function that takes a picture and changes it to HSV
def take_pic():
    # Start video capture
    cam = cv2.VideoCapture(0)

    # Grab the frame
    frame = get_frame(cam)

    # Chnage the color to RBG
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Resize the image to 200px
    frame = imutils.resize(frame, width = 200, inter = cv2.INTER_LINEAR)

    # Release the camera resource
    cam.release()
    return frame


# Function that determines the percentage of red in a photo
# Returns the percentage of Red
def determine_percRed(frame):
    # Sets the lower bound of the mask in HSV values
    mask1 = cv2.inRange(frame, (0,50,20), (5,255,255))

    # Sets the upper bound of the mask in HSV values
    mask2 = cv2.inRange(frame, (175,50,20), (180,255,255))

    # Uses bitwise_or to compare both of the masks and make a total mask of red in the image
    mask = cv2.bitwise_or(mask1,mask2)

    # Establishes the total size of the image
    sMask = mask.size

    # Calculates the percent red in the image
    percRed = ((np.sum(mask[:,:])/255)/sMask)*100
    return percRed

# Function that displays an imaeg in D1 
def show_image(frame):
    #convert back to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
    #Display the image 
    d1 = IPython.display.display("Your image will be dissplayed here", display_id =1)
    # call the function to convert array data to image
    frame = array_to_image(frame)
    d1.update(frame)

# Function that compares the percentage red to a threshold to determine if the piece is red or not
def red_or_other(percRed):
    redThresh = 3 # percent
    # Tells if red or not
    if percRed > redThresh:
        s.write("1".encode())
        print("That is red")
    else: 
        s.write("0".encode())
        print("That aint red")

s = serial.Serial("/dev/serial0",9600,timeout=2)

while True:
    if s.inWaiting() != 0
        signal = s.read(1).decode("utf-8")
        if signal == "1":
            frame = take_pic()
            percRed = determine_percRed(frame)
            red_or_other(percRed)
            show_image(frame)
