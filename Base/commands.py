import CommunicationBase
import GUI
import globals
import Joystick

# This function gets called when a command is typed into the GUI
def parse(command):
    commands = command.split(" ") # Split "command key key2" into ["command", "key", "key2"]
    print("Command: " + str(commands))
    if(commands[0].lower() == "connect"):
        if(len(commands) < 2):  # If no ip-address is given connect to default address
            commands.append("0")
        CommunicationBase.StartProcess(commands[1])
    elif(commands[0].lower() == "other"):
        globals.SendOther("other",commands)
    elif(commands[0].lower() == "ping"): # Changes the time between robot and base communication
        globals.sharedData["LocalPing"] = float(commands[1])
        globals.SendCommand(commands) # Send change to robot so it can update also
    elif(commands[0].lower() == "joystick"): # Start and stop the joystick process
        if(commands[1].lower() == "on"):
            Joystick.StartJoystickProcess()
        elif(commands[1].lower() == "off"):
            Joystick.StopJoystickProcess()
    else:
        globals.SendCommand(commands) # If its not in the list, send it to the robot for processing