from Cameras import Cameras as Cam1
from Communication import InitilizeCommunication
from StateMachine import StateMachine as SM1

# Initilize Sensors + Motors
Cameras = Cam1()
Cameras.AddCamera(640,480,.25,0,90,1,500,120)
# Cameras.AddCamera(1920,1080,0,0,1,500,120)
# Cameras.AnalizeCameras()
while(1):
    Cameras.AnalizeCameras()
    # print(Cameras.RobotLocationInfo)
    Cameras.displayPosition()
# Initilize other cameras and sensors here

# InitilizeCommunication()

StateMachine = SM1()

