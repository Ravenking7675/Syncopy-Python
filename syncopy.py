import pyrebase
import pyperclip as pc 
import platform
from uuid import getnode as get_mac
import time
import random
import string
import concurrent.futures
import threading
import atexit
from capture import create_screenshot

from subprocess import Popen, PIPE
import pyttsx3 
import os
import psutil
import pyqrcode
from art import text2art

# Defining colors

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Global variables declared here
newClip = ""
prevClip = ""

# Welcome message
welcome = text2art("Syncope")
print("----------------------------------------------------\n")
print(bcolors.BOLD+bcolors.HEADER+welcome+bcolors.ENDC)
print("\n----------------------------------------------------\n")

print(bcolors.BOLD+bcolors.OKBLUE+"Please wait while we generate your PC-ID and QR Code..\n"+bcolors.ENDC)

# service -> /Documents/service.txt



# Initializing Pyrebase
config = {
  "apiKey": "AIzaSyCpf6G0kuYL9sQRAGhUWvIh9aG2rzyD0OQ",
  "authDomain": "syncopy-project.firebaseapp.com",
  "databaseURL": "https://syncopy-project.firebaseio.com/",
  "storageBucket": "syncopy-project.appspot.com",
  "serviceAccount": service
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

# Generating uuid
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

uuid = "pc-"+get_random_alphanumeric_string(6)


# System info
pcType = platform.system()
uname = platform.uname()
pcName = uname.node

# Sending user-data
user_data = {"pcType": pcType, "pcName": pcName, "uuid": uuid, "connectedTo": "unknown"}
db.child("user_web").child(uuid).set(user_data)

#Listen to user-data change


connection_uuid = None
def stream_handler(message):

        global connection_uuid, uuid
        
        try:
            connection_uuid = message["data"]['connectedTo']
        except Exception as e:
            connection_uuid = message['data']
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and connection_uuid != "-1":
            
            print(bcolors.OKGREEN + "Connection established with {}\n".format(connection_uuid) + bcolors.ENDC)

            my_stream = db.child("clips").child(connection_uuid).stream(clip_data_stream, stream_id="clip_stream")
            db.child("status").child(uuid).set(True)
        
        if isinstance(connection_uuid, str) and connection_uuid == "-1":
            
            print(bcolors.WARNING + "Logging out...\n" + bcolors.ENDC)
            # print("Logging out...")
            cur_pid = os.getpid()
            thisSystem = psutil.Process(cur_pid)
            thisSystem.terminate()

        
def listen_to_user_data_change():
    print(bcolors.OKBLUE + ">>> Started listening to android requests...\n" + bcolors.ENDC)

    my_stream = db.child("user_web").child(uuid).stream(stream_handler, stream_id="data_change")


# clip_web > uuid > user_id > message = {"clip", "time", "history"}

# Listen to clip data change in pc
def clip_data_change_listener():
    print(bcolors.OKBLUE + ">>> Starting clip change listener...\n" + bcolors.ENDC)
    # print("Listening to clip change in PC")
    global newClip, prevClip, uuid, connection_uuid
    while True:
        try:
            if isinstance(connection_uuid, str) and connection_uuid != "unknown":

                newClip = pc.paste()
                newClip = newClip.strip()

                if(len(prevClip) >13 and prevClip[-12:] == "s*y&nc%o#p@y"):
                    newClip = pc.paste()
                    newClip = newClip.strip()
                    prevClip = newClip

                else:

                    if newClip != prevClip and len(newClip) >0:
 
                        print(bcolors.OKGREEN + ">>> Broadcasting clip to other devices...\n" + bcolors.ENDC)

                        prevClip = newClip

                        time2 = int(round(time.time() * 1000))
                        db.child("clip_web").child(connection_uuid).child("message").set({"clip": newClip, "time": time2, "history": True, "fromUUID": uuid})

        except Exception as e:
    
            print(bcolors.FAIL + ">>> Oups! Check your internet connection\n" + bcolors.ENDC)
            continue
            # e.message()               

# Listen to clip data change in FIREBASE

def clip_data_stream(message):
    # print(message["data"])
    try:
      if message['data'] is not None:
        data = message["data"]
        # print("DATA : {}".format(data))
        if isinstance(data, str):
            global newClip, prevClip, uuid, connection_uuid
        
            if(prevClip != data):

                prevClip = data+"s*y&nc%o#p@y"

                pc.copy(data)
            else:
                pass
        
        else:
            pass

      else:
          pass


    except Exception as e:
        # e.print_exc()
        print(bcolors.FAIL + ">>> Something went wrong!\n" + bcolors.ENDC)

# db.child("clip_web").child(connection_uuid).child("message").set({"clip": newClip, "time": time2, "history": True})


def clip_data_change_in_firebase_listener():
    global newClip, prevClip, uuid, connection_uuid
    
    count = 0
    
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and count == 0:
            count = 1
            
            try:
                print(bcolors.OKGREEN + ">>> Started clip data change stream...\n" + bcolors.ENDC)

                # my_stream = db.child("clips").child(connection_uuid).stream(clip_data_stream, stream_id="jgjhgj")
                my_stream = db.child("clip_web").child(connection_uuid).child("message").child("clip").stream(clip_data_stream, stream_id="jgjhgj")

            except Exception as e:
                my_stream.close()
                count=0


# Runs just before program shuts down

def logout():
    print(bcolors.WARNING + ">>> Disconnecting other devices...\n" + bcolors.ENDC)
   
    db.child("status").child(uuid).set(False)
    print(bcolors.OKGREEN + ">>> See you soon, Take care!\n" + bcolors.ENDC)

# Send screenshot

def screenshot_send_streamer():
    global newClip, prevClip, uuid, connection_uuid
    print(bcolors.OKBLUE + ">>> Starting screenshot stream...\n" + bcolors.ENDC)

    count = 0
    
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and count == 0:
            count = 1
            print(bcolors.OKGREEN + ">>> Started screenshot stream...\n" + bcolors.ENDC)

            my_stream = db.child("request").child(connection_uuid).stream(request_stream, stream_id="request_stream")


def send_screenshot():
    
  time2 = int(round(time.time() * 1000))
  print(bcolors.OKBLUE+bcolors.UNDERLINE + ">>> Grabbing resources for screen capture...\n" + bcolors.ENDC)

  create_screenshot()
  


  token = storage.child("thumbnail/{}/{}.jpg".format(connection_uuid, time2)).put("thumbnail.jpg")
  print(bcolors.OKGREEN + ">>> Thubmnail sent!\n" + bcolors.ENDC)

  thubUrl = storage.child("thumbnail/{}/{}.jpg".format(connection_uuid, time2)).get_url(None)

  db.child("thumbnail").child(connection_uuid).set({"image": thubUrl})
  
  storage.child("screenshot/{}/{}.jpg".format(connection_uuid, time2)).put("screenshot.jpg")
  print(bcolors.OKGREEN + ">>> Screenshot sent!\n" + bcolors.ENDC)

  snapUrl = storage.child("screenshot/{}/{}.jpg".format(connection_uuid, time2)).get_url(None)
  
  db.child("screenshot").child(connection_uuid).set({"image": snapUrl})


def request_stream(message):
    
      request = message["data"]
      if isinstance(request, int):
            send_screenshot()
  

# Execute commands

def execute_command(command):
    
    global uuid, connection_uuid
    
    status_time = str(round(time.time() * 1000))
    
    # repeat i am avinash
    if command[0: 6].lower() == "repeat":
        engine = pyttsx3.init() 
        engine.say(command[7:]) 
        engine.runAndWait() 

        db.child("command_status").child(uuid).child(connection_uuid).set({"status": "0"+status_time})
        
    # Opening links
    
    ## link:*browser*http://youtube.com/watch?v=dk2jk1j3kjklj21
    elif command[0:5] == "link:" :
        
        index1 = command.find("*")
        index2 = command.find("*", 6)
        query = command[index1+1: index2]
        
        process = Popen("type "+query, shell=True, 
                        universal_newlines=True, 
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        out, err = process.communicate()

        if len(err)>0:
            if err[-10 : len(err)].strip() == "not found":
                print(bcolors.FAIL+"Command does not exist!"+bcolors.ENDC)
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "1"+status_time})
        else:    
            print(bcolors.OKGREEN+">>> Opening url..."+bcolors.ENDC)
            url = query+" \""+command[index2+1:]+"\""
            process = Popen(url, shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            db.child("command_status").child(uuid).child(connection_uuid).set({"status": "0"+status_time})

    #close
    elif command[0:5] == "close":
        
        query = command[6:]
        
        process = Popen("type "+query, shell=True, 
                        universal_newlines=True, 
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        out, err = process.communicate()

        if len(err)>0:
            if err[-10 : len(err)].strip() == "not found":
                print(bcolors.FAIL+"Command does not exist!"+bcolors.ENDC)
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "1"+status_time})
        else:
            
            process = Popen("pidof "+query, shell=True, 
                        universal_newlines=True, 
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
            
            out, err = process.communicate()
            
            if len(out)>0:    
                pids = out.split(" ")
            
                for pid in pids:
                    process = Popen("kill "+pid, shell=True, 
                        universal_newlines=True, 
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)    
                print(bcolors.OKGREEN+">>> Closed {}".format(query)+bcolors.ENDC)
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "0"+status_time})
        
            else:
                print(bcolors.FAIL+">>> Application is not running!"+bcolors.ENDC)
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "2"+status_time})
            
    # Execute a command 
    else: 
        try:    
            query = command[0:command.index(" ")]
        except ValueError as v:
            query = command
            
        process = Popen("type "+query, shell=True, 
                        universal_newlines=True, 
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        out, err = process.communicate()

        if len(err)>0:
            if err[-10 : len(err)].strip() == "not found":
                print(bcolors.FAIL+"Command does not exist!"+bcolors.ENDC)
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "1"+status_time})
        
        else:

            process = Popen(command, shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            db.child("command_status").child(uuid).child(connection_uuid).set({"status": "0"+status_time})
        


# Command executor listener

def command_stream(message):

    com = message["data"]
    if isinstance(com, str):
        print(bcolors.OKGREEN + ">>> Execution the command...\n" + bcolors.ENDC)
        execute_command(com)

def command_listener():
    
    global connection_uuid, uuid
    print(bcolors.OKBLUE + ">>> Started command stream...\n" + bcolors.ENDC)
    
    print(bcolors.HEADER+"Please scan the QR Code or search the PC-ID from your android device.\n"+bcolors.ENDC)

    count = 0
    
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and count == 0:
            count = 1
            print(bcolors.OKGREEN + ">>> Started command stream...\n" + bcolors.ENDC)
            my_stream = db.child("command_web").child(uuid).child(connection_uuid).stream(command_stream, stream_id="request_stream")


if __name__ == "__main__":
    
    url = pyqrcode.create(uuid)
    
    print(bcolors.UNDERLINE+bcolors.OKGREEN+"QR CODE : \n"+bcolors.ENDC)
    print(url.terminal(quiet_zone=2))
    
    print(bcolors.UNDERLINE+bcolors.OKGREEN+"\nPC-ID : "+bcolors.ENDC)
    
    print("\n----------------------------------------------------")

    art = text2art(uuid)
    
    print(bcolors.OKGREEN+art+bcolors.ENDC)
    print("----------------------------------------------------\n")
    
    
    atexit.register(logout)
    threads = list()
        
    x = threading.Thread(target=listen_to_user_data_change, daemon=True)
    threads.append(x)
    x.start()

    
    z = threading.Thread(target=clip_data_change_listener, daemon=True)
    threads.append(z)
    z.start()
    
    clipThread = threading.Thread(target=clip_data_change_in_firebase_listener, daemon=True)
    threads.append(clipThread)
    clipThread.start()
    
    screenshot = threading.Thread(target=screenshot_send_streamer, daemon=True)
    threads.append(screenshot)
    screenshot.start()
    
    command_executor = threading.Thread(target=command_listener, daemon=True)
    threads.append(command_executor)
    command_executor.start()
    
    for index, thread in enumerate(threads):
        thread.join()
        
    
