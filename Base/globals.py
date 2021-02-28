from multiprocessing import Manager

def initilizeGlobals():
    manager = Manager()
    # global dataToSend
    # global readyToSend
    # global dataRecieved
    # global newDataRecieved
    global sharedData
    # dataToSend = manager.dict()
    sharedData = manager.dict()
    sharedData["DataToSend"] = {}
    # readyToSend = False
    # dataRecieved = manager.dict()
    sharedData["DataRecieved"] = {}
    # newDataRecieved = Value('i',0)
    sharedData["NewDataRecieved"] = False
    sharedData["LocalPing"] = .1
    sharedData["LastConnectTime"] = 0
    sharedData["ConnectedAddress"] = None

def SendOther(key,command):
    if key in sharedData["DataToSend"]:
        tmp = sharedData["DataToSend"]
        if key not in tmp:
            tmp[key] = []
        tmp[key].append(command)
        sharedData["DataToSend"] = tmp
    else:
        sharedData["DataToSend"] = {key: [command]}

def SendCommand(command):
    SendOther("commands",command)