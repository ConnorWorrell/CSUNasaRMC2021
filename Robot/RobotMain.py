from Cameras import Cameras as Cam1
import CommunicationRobot
from multiprocessing import Process
from StateMachine import StateMachine as SM1

# Initilize Sensors + Motors
# Cameras = Cam1()
# Cameras.AddCamera(640,480,.25,0,90,1,500,120)
# Cameras.AddCamera(1920,1080,0,0,1,500,120)
# Cameras.AnalizeCameras()
# while(1):
#     Cameras.AnalizeCameras()
#     # print(Cameras.RobotLocationInfo)
#     Cameras.displayPosition()
# Initilize other cameras and sensors here

# ListenForData()
if __name__ == '__main__':
    CommunicationRobot.InitilizeCommunication()
    print(CommunicationRobot.CheckRecieveData())
    CommunicationRobot.SendData((1,2,3,4,5,6,7,8,9,10,1111))
    # p = Process(target = ListenForData, args = ())
    # p.start()

# CommunicationRobot.SendData((1,2,3,4,5,6,7,8,9,101,12))
# StateMachine = SM1()

