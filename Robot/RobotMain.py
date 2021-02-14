from Cameras import Cameras as Cam1
from Communication import InitilizeCommunication
from StateMachine import StateMachine as SM1

# Initilize Sensors + Motors
Cameras = Cam1()
Cameras.AddCamera(1920,1080)

# Initilize other cameras and sensors here

# InitilizeCommunication()

StateMachine = SM1()

