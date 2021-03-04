from multiprocessing import Manager, Lock

def initilizeGlobals():
    manager = Manager()
    global sharedData
    sharedData = manager.dict()
    sharedData["DataToSend"] = {}
    sharedData["DataRecieved"] = {}
    sharedData["NewDataRecieved"] = False
    sharedData["LocalPing"] = .1
    sharedData["LastConnectTime"] = 0
    sharedData["ConnectedAddress"] = None
    sharedData["ConnectionStatus"] = 2  # Reconnecting
    sharedData["JoystickOn"] = False

    global ThreadLocker
    ThreadLocker = Lock()

# TODO this is communication stuff, so it should really be in the communicationbase.py
# Add a key and command to be sent to the robot
def SendOther(key,command):
    if key in sharedData["DataToSend"]:
        tmp = sharedData["DataToSend"]
        if key not in tmp:
            tmp[key] = []
        tmp[key].append(command)
        sharedData["DataToSend"] = tmp
    else:
        sharedData["DataToSend"] = {key: [command]}

# Send a command with the key "command"
def SendCommand(command):
    SendOther("commands",command)