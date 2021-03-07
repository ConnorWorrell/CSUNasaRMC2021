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
                CommandEval(key,comm,lock)

# Handels what to do with each command
def CommandEval(key,comm,lock):
    print("Parse: " + key + " " + str(comm))
    if(key == 'commands'):
        if(comm[0] == "ping"):
            lock.acquire()
            globals.sharedData["Ping"] = float(comm[1])
            lock.release()
        elif(comm[0].lower() == "motorleft"):
            lock.acquire()
            globals.sharedMotorSpeedData["RLSpeed"] = float(comm[1])
            globals.sharedMotorSpeedData["FLSpeed"] = float(comm[1])
            lock.release()
            print("Left Speed Set " + str(comm[1]))
        elif (comm[0].lower() == "motorright"):
            lock.acquire()
            globals.sharedMotorSpeedData["RRSpeed"] = float(comm[1])
            globals.sharedMotorSpeedData["FRSpeed"] = float(comm[1])
            lock.release()
            print("Right Speed Set " + str(comm[1]))
    if(key == 'Joystick'):
        # print("joy",key,comm)
        lock.acquire()
        globals.sharedMotorSpeedData["RLSpeed"] = float(comm[1] / 33000)
        globals.sharedMotorSpeedData["RRSpeed"] = float(comm[3] / 33000)
        globals.sharedMotorSpeedData["FLSpeed"] = float(comm[1] / 33000)
        globals.sharedMotorSpeedData["FRSpeed"] = float(comm[3] / 33000)
        lock.release()
    # elif(comm[0] == "motor"):
    #     print("Starting motor")
    #     globals.motors.wheel(3, .5)
    # elif (comm[0] == "stop"):
    #     print("Stopping motor")
    #     globals.motors.wheel(3, .0)

# This is called if the robot has not from the base in 3 times the ping time
def StopEverything():
    lock = globals.ThreadLock
    lock.acquire()
    globals.sharedMotorSpeedData["RLSpeed"] = 0
    globals.sharedMotorSpeedData["RRSpeed"] = 0
    globals.sharedMotorSpeedData["FLSpeed"] = 0
    globals.sharedMotorSpeedData["FRSpeed"] = 0
    lock.release()
    # print("Timedout, Stopping Everything")
    pass