import atexit

def logout():
    print("I am dying")

if __name__ == "__main__":
    
    atexit.register(logout)
    print("Hey i am alive")

    while(True):
        pass