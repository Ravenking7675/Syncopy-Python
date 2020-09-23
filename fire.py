import pyrebase
import pyperclip as pc 

from uuid import getnode as get_mac


prevClip = ""
newClip = ""

config = {
  "apiKey": "AIzaSyCpf6G0kuYL9sQRAGhUWvIh9aG2rzyD0OQ",
  "authDomain": "syncopy-project.firebaseapp.com",
  "databaseURL": "https://syncopy-project.firebaseio.com/",
  "storageBucket": "syncopy-project.appspot.com",
  "serviceAccount": "syncopy-project-firebase-adminsdk-t8rke-f1c567139e.json"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

data = "hello"

# 0mWIdbEuDoTn0S60EhGlQUOo0SF3

# Get data one by one

users = db.child("clip").child("0mWIdbEuDoTn0S60EhGlQUOo0SF3").order_by_key().limit_to_last(1).get()
print(users.val())


# Stream Data

def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    
    try:
      data = message['data']
      print(data["clip"])
      newClip = message["data"]['clip']
      # if newClip != prevClip:
      pc.copy(newClip)
      prevClip = newClip
    except Exception as e:
      print("something went wrong")
  
    newClip = message["data"]['clip']
    if newClip != prevClip:
          pc.copy(newClip)
          prevClip = newClip
    
my_stream = db.child("clip").child("0mWIdbEuDoTn0S60EhGlQUOo0SF3").stream(stream_handler)


