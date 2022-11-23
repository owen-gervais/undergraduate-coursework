import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import time
from math import floor
import json, requests
import os

global model
	
# --------------------------------- Tensorflow Model -----------------------------------


# Loads the keras model created from Teachable Machines
def initMachine():
	global model
	model = tensorflow.keras.models.load_model('/Users/apple/Downloads/converted_keras-3/keras_model.h5')
	return 1



def askMachine(path):
# Input: Path to the testing image file
# Output: Returns the comparison against the loaded keras model

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(path)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    result = prediction.tolist()
    return result



# ----------------------------------- SystemLink ---------------------------------------
     

# Defines the Systemlink URL base and headers. 
def SL_setup(Key):
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     #print('Got URL and Headers')
     return urlBase, headers
     


# Put call in order to push back the state of the tag. 
def Put_SL(Tag, Type, Value,place):
     if place == 'home':
          key = 'Ngkq_SWxIHfOGbqtaKOlJ6OVDZGLuTwlJa2SB3SjEF'
     else:
          key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
     urlBase, headers = SL_setup(key)
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = requests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply



# Get call in order to grab the state of the desired tag.
def Get_SL(Tag,place):
     if place == 'home':
          key = 'Ngkq_SWxIHfOGbqtaKOlJ6OVDZGLuTwlJa2SB3SjEF'
     else:
          key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
     urlBase, headers = SL_setup(key)
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = requests.get(urlValue,headers=headers).text
          data = json.loads(value)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result

# ------------------------------------- SNAPR ----------------------------------------

# Defines the urlbase for requests
urlBase = "http://192.168.1.24/"

#Put_SL('Start01','BOOLEAN','true','school')


# Gets an image from the Raspberry Pi SNAPR server and downloads to the specified path
def Get_Image():
     try:
          value = requests.get(urlBase + 'download')
          f = open('/Users/apple/Desktop/Final Documentation/TestingImage/test.jpg','wb')
          f.write(value.content)
          f.close()
          result = True
     except Exception as e:
          print(e)
          result = False
     return result



def isBall(result): 
# Input: Result to the system after running the askMachine() 
# Output: Gives a boolean true or false in STR format for System link tags 
    result = askMachine(path)
    percBall = floor(result[0][0]*100)
    percNo = floor(result[0][1]*100)

    print('Ball:', percBall)
    print('No Ball', percNo)

    if percBall > 85:
        return 'true'
    return 'false' 


#-------------------------------- Systemlink App Key -----------------------------------
# classkey: bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0
# personalkey: Ngkq_SWxIHfOGbqtaKOlJ6OVDZGLuTwlJa2SB3SjEF

#Key = 'Ngkq_SWxIHfOGbqtaKOlJ6OVDZGLuTwlJa2SB3SjEF'

#---------------------------------------------------------------------------------------


# Initializes the Machine 
initMachine()
path = '/Users/apple/Desktop/Final Documentation/TestingImage/test.jpg'
update = 'true'


# Live loop for testing the images
while True:

    # Checks for an update to the Systemlink Tag and prints if it is waiting for response
    runTensor = Get_SL('RunTensor','home')
    print('')
    print('Waiting for response......')
    print('')

    

    # Main loop operation 
    while runTensor == 'true':

          # Grabs the image from the Raspberry Pi
          Get_Image()

          try:
               # Checks the byte size of the image and then only continues if the image is above the threshold
               # This works against the Rasberry Pi slow loading on to the page and allows for the system
               # to work every time.
               byteSize = os.stat('/Users/apple/Desktop/Final Documentation/TestingImage/test.jpg').st_size
               # print('ByteSize:',byteSize/1000)
               if (byteSize/1000) > 180:
                    print('--------------------')
                    print('Image Fully Loaded!')
                    print('--------------------')


                    # Gets the result of the tensorFlow testing
                    path = '/Users/apple/Desktop/Final Documentation/TestingImage/test.jpg'
                    result = askMachine(path)
                    runCLAW = isBall(result)


                    # Puts the rest of the info to the Systemlink cloud
                    Put_SL('update','STRING',update,'home')
                    Put_SL('runCLAW', 'STRING', runCLAW,'home')
                    print('Switch to the Air')
                    break
               else:
                    print('')
                    print('Redownloading......')
                    print('')
          except:
               print('Error')




