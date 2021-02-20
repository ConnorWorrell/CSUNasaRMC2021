import CommunicationBase
import GUI

def parse(command):
    commands = command.split(" ")
    print("Command: " + str(commands))
    if(commands[0].lower() == "connect"):
        if(len(commands) < 2):
            commands.append(None)
        CommunicationBase.InitilizeCommunication(commands[1])
        # CommunicationBase.StartProcess(commands[1])
    elif(commands[0].lower() == "send"):
        CommunicationBase.SendData([1,2,3,4,5,[1,2,3,4,5]]*1000)
        print(CommunicationBase.CheckRecieveData())