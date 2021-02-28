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
    sharedData["DataToSend"] = {"CameraFrames":[]}
    # readyToSend = False
    # dataRecieved = manager.dict()
    sharedData["DataRecieved"] = {"commands":[]}
    # newDataRecieved = Value('i',0)
    sharedData["NewDataRecieved"] = False
    sharedData["Ping"] = .1
    sharedData["LastConnectTime"] = 0