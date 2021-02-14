from cv2 import *

class Cameras:

    def __init__(self):
        self.CameraStorage = []

    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
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
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    def AddCamera(self,ResWidth,ResHeight):
        cam = VideoCapture(len(self.CameraStorage))
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, ResWidth)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT,ResHeight)
        self.CameraStorage.append(cam)

    def AnalizeCameras(self):
        for Camera in self.CameraStorage:
            s, img = Camera.read()
            cv2.imshow("Result", self.image_resize(img, 720, 480))
        cv2.waitKey(0)