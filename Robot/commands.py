import globals

# Called when new data is recieved
def ParseCommands():
    lock = globals.ThreadLock
    lock.acquire()
    data = globals.sharedData.copy()
    if data["NewDataRecieved"] == True:
        globals.sharedData["NewDataRecieved"] = False
        globals.sharedData["DataRecieved"] = {}
    lock.release()
    if data["NewDataRecieved"] == True:
        for key in data["DataRecieved"]:
            for comm in data["DataRecieved"][key]:
                CommandEval(key,comm)

# Handels what to do with each command
def CommandEval(key,comm):
    print("Parse: " + key + " " + str(comm))
    if(comm[0] == "ping"):
        globals.sharedData["Ping"] = float(comm[1])
    elif(comm[0] == "motor"):
        print("Starting motor")
        globals.motors.wheel(3, .5)
    elif (comm[0] == "stop"):
        print("Stopping motor")
        globals.motors.wheel(3, .0)

# This is called if the robot has not from the base in 3 times the ping time
def StopEverything():
    # print("Timedout, Stopping Everything")
    pass