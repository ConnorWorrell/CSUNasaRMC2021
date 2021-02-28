# Cameras.AnalizeCameras()
# while(1):
#     Cameras.AnalizeCameras()
#     # print(Cameras.RobotLocationInfo)
#     Cameras.displayPosition()
# Initilize other cameras and sensors here

# ListenForData()



if __name__ == '__main__':
    from Cameras import Cameras as Cam1
    import CommunicationRobot
    from multiprocessing import Process
    from StateMachine import StateMachine as SM1
    import globals
    from cv2 import *
    import commands


    def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    # Initilize Sensors + Motors
    Cameras = Cam1()
    # Cameras.AddCamera(640,480,.25,0,90,1,500,120)
    Cameras.AddCamera(1920, 1080, 0, 0, 0, 1, 500, 120)
    Cameras.AddCamera(1920, 1080, 0, 0, 0, 1, 500, 120)
    print(Cameras.CameraStorage)

    globals.initilizeGlobals()
    sharedData = globals.sharedData
    # CommunicationRobot.InitilizeCommunication()
    # print(CommunicationRobot.CheckRecieveData())
    # CommunicationRobot.SendData((1,2,3,4,5,6,7,8,9,10,1111))
    print(sharedData)
    p = Process(target = CommunicationRobot.StartCommunication, args = (sharedData,))
    p.start()
    import random
    import time
    while True:
        ping = time.time() - sharedData["LastConnectTime"]
        if(ping > 5):
            commands.StopEverything()
            time.sleep(1)
        else:
            # print("updates")
            # print(sharedData)
            # Cameras.UpdateFrameData()
            Cameras.AnalizeCameras()
            Encoded = []
            for i in Cameras.LastFrames:
                # print(cv2.imencode(".jpg",i,[int(cv2.IMWRITE_JPEG_QUALITY),90]))
                img_r = image_resize(i,200,200)
                Encoded.append(cv2.imencode(".jpg",img_r,[int(cv2.IMWRITE_JPEG_QUALITY),90])[1].tobytes())
            sharedData["DataToSend"] = {"CameraFrames" : Encoded}
            # print(globals.sharedData["DataRecieved"]["commands"])
            commands.ParseCommands()

            # time.sleep(1)

# CommunicationRobot.SendData((1,2,3,4,5,6,7,8,9,101,12))
# StateMachine = SM1()

