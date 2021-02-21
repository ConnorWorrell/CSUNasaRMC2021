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