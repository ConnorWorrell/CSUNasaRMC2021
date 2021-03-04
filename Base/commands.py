import CommunicationBase
import GUI
import globals
import Joystick

def parse(command):
    commands = command.split(" ")
    print("Command: " + str(commands))
    if(commands[0].lower() == "connect"):
        if(len(commands) < 2):
            commands.append("0")
        CommunicationBase.StartProcess(commands[1])
    elif(commands[0].lower() == "other"):
        globals.SendOther("other",commands)
    elif(commands[0].lower() == "ping"):
        globals.sharedData["LocalPing"] = float(commands[1])
        globals.SendCommand(commands)
    elif(commands[0].lower() == "joystick"):
        if(commands[1].lower() == "on"):
            Joystick.StartJoystickProcess()
        elif(commands[1].lower() == "off"):
            Joystick.StopJoystickProcess()
    else:
        globals.SendCommand(commands)
        # if "commands" in globals.sharedData["DataToSend"]:
        #     tmp = globals.sharedData["DataToSend"]["commands"]
        #     tmp.append(commands)
        #     globals.sharedData["DataToSend"] = {"test":tmp}
        # else:
        #     globals.sharedData["DataToSend"] = {"commands": [commands]}
        # CommunicationBase.StartProcess(commands[1])
    # elif(commands[0].lower() == "send"):
    #     CommunicationBase.SendData([1,2,3,4,5,[1,2,3,4,5]]*1000)
    #     print(CommunicationBase.CheckRecieveData())