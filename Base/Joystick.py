from inputs import get_gamepad
import globals
from multiprocessing import Process

# Joystick handels updating the joystick values
class Joystick:
    def __init__(self): # Assume all buttons and joysticks start unpressed or centered
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

    # This waits for something in the joystick to change, and when it does, it updates the class variables
    # It returns the new joystick
    def CheckForChanges(self):
        # Remove Sync events, these don't seem to be useful, they are just duplicates of the Absolute or Key events
        prunedEvents = []
        while prunedEvents == []:
            try:
                events = get_gamepad()
            except:
                print("Joystick Lost")
                break
            for event in events:
                if event.ev_type != "Sync":
                    prunedEvents.append(event)

        # Update variables
        for event in prunedEvents:
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

# Start a process that handels the joystick
def StartJoystick(sharedData,lock):
    lock.acquire()
    sharedData["JoystickOn"] = True
    lock.release()

    joy = Joystick()
    while (sharedData["JoystickOn"] == True):
        Changes = joy.CheckForChanges() # Wait for changes
        if sharedData["JoystickOn"] == False: # Check if joystick off command recieved
            break

        # Send changes to the robot
        if Changes is not False:
            lock.acquire()
            tmp = sharedData["DataToSend"]
            if "Joystick" not in tmp.keys():
                tmp["Joystick"] = []
            tmp["Joystick"].append(Changes)
            sharedData["DataToSend"] = tmp
            lock.release()

# This is the command that is called by the GUI to start the joystick process
def StartJoystickProcess():
    global joyProcess
    joyProcess = Process(target=StartJoystick, args=(globals.sharedData,globals.ThreadLocker))
    joyProcess.start()

# Function called by the gui to stop the joystick process
def StopJoystickProcess():
    sharedData = globals.sharedData
    lock = globals.ThreadLocker
    lock.acquire()
    sharedData["JoystickOn"] = False # This flag is checked duirng the joystick process
    lock.release()

if __name__ == '__main__':
    joy = Joystick()
    while(1):
        Changes = joy.CheckForChanges()
        if Changes is not False:
            print(Changes)