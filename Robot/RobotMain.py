
# Main robot program
if __name__ == '__main__':
    from Cameras import Cameras as Cam1
    import CommunicationRobot
    from multiprocessing import Process
    import globals
    from cv2 import *
    import commands
    import time

    # resize image but maintain aspect ratio
    # TODO move this into cameras
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

    globals.initilizeGlobals()
    sharedData = globals.sharedData
    lock = globals.ThreadLock

    # Start communication process
    p = Process(target = CommunicationRobot.StartCommunication, args = (sharedData,lock,))
    p.start()

    while True:
        # Calculate ping and determine if we need to stop the robot for safety reasons
        ping = time.time() - sharedData["LastConnectTime"]
        if(ping > 5): # timed out TODO change to based on expected ping
            commands.StopEverything()
            time.sleep(1)
        else: # ping is good
            # Take photos, and to que to be sent to base todo move this to cameras
            Cameras.AnalizeCameras()
            Encoded = []
            for i in Cameras.LastFrames:
                img_r = image_resize(i,200,200)
                Encoded.append(cv2.imencode(".jpg",img_r,[int(cv2.IMWRITE_JPEG_QUALITY),90])[1].tobytes())
            sharedData["DataToSend"] = {"CameraFrames" : Encoded}

            # check for commands from base
            commands.ParseCommands()