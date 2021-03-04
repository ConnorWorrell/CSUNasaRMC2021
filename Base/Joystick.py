from inputs import get_gamepad
import globals
from multiprocessing import Process
import time

class Joystick:
    def __init__(self):
        self.ABS_X = 0
        self.ABS_Y = 0
        self.ABS_RX = 0
        self.ABS_RY = 0
        self.BTN_NORTH = 0
        self.BTN_SOUTH = 0
        self.BTN_EAST = 0
        self.BTN_WEST = 0
        self.ABS_HAT0X = 0
        self.ABS_HAT0Y = 0
        self.BTN_SELECT = 0
        self.BTN_START = 0
        self.ABS_RZ = 0
        self.BTN_TR = 0
        self.ABS_Z = 0
        self.BTN_TL = 0
        self.BTN_THUMBR = 0
        self.BTN_THUMBL = 0
        
    def CheckForChanges(self):
        prunedEvents = []
        while prunedEvents == []:
            events = get_gamepad()
            for event in events:
                if event.ev_type != "Sync":
                    prunedEvents.append(event)

        for event in prunedEvents:
            # print(event.ev_type, event.code, event.state)
            if (event.ev_type == "Absolute" or event.ev_type == "Key"):
                if (event.code == "ABS_X"):
                    self.ABS_X = event.state
                elif (event.code == "ABS_Y"):
                    self.ABS_Y = event.state
                elif (event.code == "ABS_RX"):
                    self.ABS_RX = event.state
                elif (event.code == "ABS_RY"):
                    self.ABS_RY = event.state
                elif (event.code == "BTN_NORTH"):
                    self.BTN_NORTH = event.state
                elif (event.code == "BTN_SOUTH"):
                    self.BTN_SOUTH = event.state
                elif (event.code == "BTN_EAST"):
                    self.BTN_EAST = event.state
                elif (event.code == "BTN_WEST"):
                    self.BTN_WEST = event.state
                elif (event.code == "ABS_HAT0X"):
                    self.ABS_HAT0X = event.state
                elif (event.code == "ABS_HAT0Y"):
                    self.ABS_HAT0Y = event.state
                elif (event.code == "BTN_SELECT"):
                    self.BTN_SELECT = event.state
                elif (event.code == "BTN_START"):
                    self.BTN_START = event.state
                elif (event.code == "ABS_RZ"):
                    self.ABS_RZ = event.state
                elif (event.code == "ABS_Z"):
                    self.ABS_Z = event.state
                elif (event.code == "BTN_TL"):
                    self.BTN_TL = event.state
                elif (event.code == "BTN_TR"):
                    self.BTN_TR = event.state
                elif (event.code == "BTN_THUMBR"):
                    self.BTN_THUMBR = event.state
                elif (event.code == "BTN_THUMBL"):
                    self.BTN_THUMBL = event.state

        return([self.ABS_X, self.ABS_Y, self.ABS_RX, self.ABS_RY, self.BTN_NORTH, self.BTN_SOUTH, self.BTN_EAST, self.BTN_WEST, self.ABS_HAT0X, self.ABS_HAT0Y,
                  self.BTN_SELECT, self.BTN_START, self.ABS_RZ, self.ABS_Z, self.BTN_TL, self.BTN_TR, self.BTN_THUMBR, self.BTN_THUMBL])

def StartJoystick(sharedData,lock):
    lock.acquire()
    sharedData["JoystickOn"] = True
    lock.release()

    joy = Joystick()
    while (sharedData["JoystickOn"] == True):
        Changes = joy.CheckForChanges()
        if sharedData["JoystickOn"] == False:
            break

        if Changes is not False:
            print(Changes)
            lock.acquire()
            tmp = sharedData["DataToSend"]
            if "Joystick" not in tmp.keys():
                tmp["Joystick"] = []
            tmp["Joystick"].append(Changes)
            sharedData["DataToSend"] = tmp
            lock.release()
        print(sharedData["DataToSend"])

def StartJoystickProcess():
    global joyProcess
    joyProcess = Process(target=StartJoystick, args=(globals.sharedData,globals.ThreadLocker))
    joyProcess.start()

def StopJoystickProcess():
    sharedData = globals.sharedData
    lock = globals.ThreadLocker
    lock.acquire()
    sharedData["JoystickOn"] = False
    lock.release()

if __name__ == '__main__':
    joy = Joystick()
    while(1):
        Changes = joy.CheckForChanges()
        if Changes is not False:
            print(Changes)