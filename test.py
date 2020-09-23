# import pyrebase
# import pyperclip as pc 
# import platform
# from uuid import getnode as get_mac
# import time
# import random
# import string
# import concurrent.futures
# import threading
# from syncopy import storage, db, connection_uuid
# from capture import create_screenshot

# # config = {
# #   "apiKey": "AIzaSyAmRlZuwAspOzBd30dGlUaOg_PKMvxlheo",
# #   "authDomain": "fuckyou-d3389.firebaseapp.com",
# #   "databaseURL": "https://fuckyou-d3389.firebaseio.com/",
# #   "storageBucket": "fuckyou-d3389.appspot.com",
# #   "serviceAccount": "fuckyou-d3389-firebase-adminsdk-6jxd7-1c042e7d54.json"
# # } 

# # firebase = pyrebase.initialize_app(config)
# # db = firebase.database()
# # storage = firebase.storage()

# # as admin

# def send_screenshot():

#   time2 = int(round(time.time() * 1000))
  
#   create_screenshot()
  
#   print("Starts")

#   token = storage.child("thumbnail/{}/{}.jpg".format(connection_uuid, time2)).put("thumbnail.jpg")
#   print("1st Done")
#   thubUrl = storage.child("thumbnail/{}/{}.jpg".format(connection_uuid, time2)).get_url(None)
#   print(thubUrl)
  
#   db.child("thumbnail").child(connection_uuid).set({"image": thubUrl})
  
#   storage.child("screenshot/{}/{}.jpg".format(connection_uuid, time2)).put("screenshot.jpg")
#   print("2nd Done")
#   snapUrl = storage.child("screenshot/{}/{}.jpg".format(connection_uuid, time2)).get_url(None)
#   print(snapUrl)
  
#   db.child("screenshot").child(connection_uuid).set({"image": snapUrl})

# def request_stream(message):
#       print(message["data"])
#       request = message["data"]
#       if isinstance(request, int):
#             print("Yeah!")
#             send_screenshot()
  
# # if __name__ == "__main__":
  
# #   my_stream = db.child("request").child("uuid").stream(request_stream, stream_id="request_stream")

# #   # send_screenshot()



# ------------------------------------------------------------------------------

from subprocess import Popen, PIPE

command = input("Enter a command to execute : ")
try:
    process = Popen(command, shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # process.communicate()
    # print(out)
    # print(err)
except Exception as e:
    print("Command does not exist")
    
# pidof <name>
# kill <pid>


# Import the required module for text 
# to speech conversion 

# importing the pyttsx library 
import pyttsx3 
  
# initialisation 
engine = pyttsx3.init() 
  
# testing 
engine.say("Hello master Avinash, nice to meet you") 

engine.runAndWait() 
