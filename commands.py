from subprocess import Popen, PIPE
import pyttsx3 

from time import sleep
from syncopy import send_screenshot

db="Database"
uuid=""
connection_uuid=""

#check the command

# command = input("Enter the command : ")

def execute_command(command):
    # repeat i am avinash
    if command[0: 6].lower() == "repeat":
        engine = pyttsx3.init() 
        engine.say(command[7:]) 
        engine.runAndWait() 

        db.child("command_status").child(uuid).child(connection_uuid).set({"status": 0})
        
    # Opening links
    elif command[0:5] == "link:" :
        print("Opening link")
        process = Popen("chromium "+command[5:], shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        db.child("command_status").child(uuid).child(connection_uuid).set({"status": 0})

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
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": 1})
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
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": 0})
        
            else:
                print("Program is not running")
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": 2})
            
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
                db.child("command_status").child(uuid).child(connection_uuid).set({"status": 1})
        
        else:
            print("command exists")
            
            # Execute the command
            
            process = Popen(command, shell=True, universal_newlines=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            db.child("command_status").child(uuid).child(connection_uuid).set({"status": 0})
        
# xdg-screensaver lock