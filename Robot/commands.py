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

def StopEverything():
    print("Timedout, Stopping Everything")
