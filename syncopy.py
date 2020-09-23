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


#Global variables declared here
newClip = ""
prevClip = ""
clip_lock = threading.Lock()

# Initializing Pyrebase
config = {
  "apiKey": "AIzaSyCpf6G0kuYL9sQRAGhUWvIh9aG2rzyD0OQ",
  "authDomain": "syncopy-project.firebaseapp.com",
  "databaseURL": "https://syncopy-project.firebaseio.com/",
  "storageBucket": "syncopy-project.appspot.com",
  "serviceAccount": "syncopy-project-firebase-adminsdk-t8rke-f1c567139e.json"
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
print("UUID : {}".format(uuid))

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
        if isinstance(connection_uuid, str) and connection_uuid != "unknown":
            print("Connection established with {}".format(connection_uuid))
            my_stream = db.child("clip").child(connection_uuid).stream(clip_data_stream, stream_id="clip_stream")
            db.child("status").child(uuid).set(True)

        
def listen_to_user_data_change():
    print("Starting listening to user data change...")
    my_stream = db.child("user_web").child(uuid).stream(stream_handler, stream_id="data_change")

# Sending alive token
# def send_alive_token():
#     print("Looking for the user to connect...")
#     global connection_uuid
#     global uuid
#     # if isinstance(connection_uuid, str) and connection_uuid != "unknown":
#     while True:
#         if isinstance(connection_uuid, str) and connection_uuid != "unknown":
#             print("Sending isAlive token...")
#             time2 = int(round(time.time() * 1000))
#             db.child("alive").child(uuid).set({"isAlive": time2})
#             time.sleep(5)
            

# Listen to clip data change in pc
def clip_data_change_listener():
    print("Listening to clip change in PC")
    global newClip, prevClip, uuid, connection_uuid
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown":
            # clip_lock.acquire()
            newClip = pc.paste()
            newClip = newClip.strip()
                        
            # clip_lock.release()
            # clip_lock.acquire()
            
            if(len(prevClip) >13 and prevClip[-12:] == "s*y&nc%o#p@y"):
                newClip = pc.paste()
                newClip = newClip.strip()
                prevClip = newClip
                # print("This clip is from other user")
                pass
            else:
                # print("Concatination is : "+prevClip[-12:])
                if newClip != prevClip and len(newClip) >0:
                    print("Sending clip to firebase... : ")
                    print("[SCTF] new clip is : {} and previous clip is : {}".format(newClip, prevClip))
                    prevClip = newClip
                    # clip_lock.release()
                    time2 = int(round(time.time() * 1000))
                    db.child("clip").child(connection_uuid).push({"clip": newClip, "time": time2, "history": True})
                    # clip_lock.acquire()
                    print("Broke the lock im out")
                # clip_lock.release()
                

# Listen to clip data change in FIREBASE

def clip_data_stream(message):

    print("Starting listning to clips")
    
    try:
      if message['data'] is not None:
        data = list(message['data'].values())[0]
        print("DATA : {}".format(data))
        if isinstance(data, str):
            global newClip, prevClip, uuid, connection_uuid
        
            if(prevClip != data):
                print("NEW CLIP : {}".format(data))
                print("new clip is {} and previous clip is {}".format(newClip, prevClip))

                clip_lock.acquire()
                print("Locked the clip")
                prevClip = data+"s*y&nc%o#p@y"

                pc.copy(data)
                print("releasing the lock")
                clip_lock.release()
            else:
                print("Clip is same")
        
        else:
            print("CLIP DATA IS NOT A STRING")
      else:
        print("DATA IS NONE")

    except Exception as e:
        
      e.message()
      print("something went wrong in clip_data_stream")
  
    
def clip_data_change_in_firebase_listener():
    global newClip, prevClip, uuid, connection_uuid
    
    count = 0
    
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and count == 0:
            count = 1
            print("Listening to clip data change in firebase : {}".format(connection_uuid))
            my_stream = db.child("clip").child(connection_uuid).stream(clip_data_stream)
            print("Clip listener started...")


# Runs just before program shuts down

def logout():
    print("Shutting down...")
    db.child("status").child(uuid).set(False)

# Send screenshot

def screenshot_send_streamer():
    global newClip, prevClip, uuid, connection_uuid
    print("Screenshot stream starting...")
    count = 0
    
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and count == 0:
            count = 1
            print("Screenshot stream starts")
            my_stream = db.child("request").child(connection_uuid).stream(request_stream, stream_id="request_stream")


def send_screenshot():
    
  time2 = int(round(time.time() * 1000))
  
  create_screenshot()
  
  print("Starts")

  token = storage.child("thumbnail/{}/{}.jpg".format(connection_uuid, time2)).put("thumbnail.jpg")
  print("1st Done")
  thubUrl = storage.child("thumbnail/{}/{}.jpg".format(connection_uuid, time2)).get_url(None)
  print(thubUrl)
  
  db.child("thumbnail").child(connection_uuid).set({"image": thubUrl})
  
  storage.child("screenshot/{}/{}.jpg".format(connection_uuid, time2)).put("screenshot.jpg")
  print("2nd Done")
  snapUrl = storage.child("screenshot/{}/{}.jpg".format(connection_uuid, time2)).get_url(None)
  print(snapUrl)
  
  db.child("screenshot").child(connection_uuid).set({"image": snapUrl})


def request_stream(message):
      print(message["data"])
      request = message["data"]
      if isinstance(request, int):
            print("Yeah!")
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
        
        print("Browser : "+query)
        
        process = Popen("type "+query, shell=True, 
                        universal_newlines=True, 
                        stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        out, err = process.communicate()

        if len(err)>0:
            if err[-10 : len(err)].strip() == "not found":
                print("Command does not exist")
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "1"+status_time})
        else:    
            print("Opening link")
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
                print("Command does not exist")
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "1"+status_time})
        else:
            print("command exists")
            
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
                
                print("Closed {}".format(query))
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "0"+status_time})
        
            else:
                print("Program is not running")
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
                print("Command does not exist")
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": "1"+status_time})
        
        else:
            print("command exists")
            
            # Execute the command
            
            process = Popen(command, shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            db.child("command_status").child(uuid).child(connection_uuid).set({"status": "0"+status_time})
        


# Command executor listener

def command_stream(message):
    print(message["data"])
    com = message["data"]
    if isinstance(com, str):
        print("Execution of command starts...")
        execute_command(com)

def command_listener():
    
    global connection_uuid, uuid
    
    print("Command stream starting...")
    count = 0
    
    while True:
        if isinstance(connection_uuid, str) and connection_uuid != "unknown" and count == 0:
            count = 1
            print("Command stream starts now")
            my_stream = db.child("command_web").child(uuid).child(connection_uuid).stream(command_stream, stream_id="request_stream")


if __name__ == "__main__":
    
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
        
        
