import globals

def ParseCommands():
    data = globals.sharedData
    if data["NewDataRecieved"] == True:
        for key in data["DataRecieved"]:
            for comm in data["DataRecieved"][key]:
                CommandEval(key,comm)
        data["NewDataRecieved"] = False
        globals.sharedData["DataRecieved"] = {}

def CommandEval(key,comm):
    print("Parse: " + key + " " + str(" ".join(comm)))
    if(comm[0] == "ping"):
        globals.sharedData["Ping"] = float(comm[1])
    elif(comm[0] == "motor"):
        print("Starting motor")
        globals.motors.wheel(3, .5)
    elif (comm[0] == "stop"):
        print("Stopping motor")
        globals.motors.wheel(3, .0)

def StopEverything():
    # print("Timedout, Stopping Everything")
    pass