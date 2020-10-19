#https://www.youtube.com/watch?v=SrZuwM705yE&ab_channel=Murtaza%27sWorkshop-RoboticsandAI
# https://www.youtube.com/watch?v=dQrUilGMz_k&ab_channel=VipulVaibhaw

from cv2 import *
import numpy as np
from pyzbar.pyzbar import decode,ZBarSymbol

fromCamera = True

def Analysis(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for barcode in decode(gray):#,symbols=[ZBarSymbol.QRCODE]):
        print(barcode)
        myData = barcode.data.decode('utf-8')
        pts=np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
    cv2.imshow("Result",img)
    cv2.waitKey(1)

if(fromCamera):
    cam = VideoCapture(0)

    # cam = VideoCapture(0,cv2.CAP_DSHOW)
    # cam.set(cv2.CAP_PROP_FPS, 30.0)
    # cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))
    # cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # feature_params = dict(maxCorners=100,
    #                       qualityLevel=0.3,
    #                       minDistance=7,
    #                       blockSize=7)
    #
    # # Parameters for lucas kanade optical flow
    # lk_params = dict(winSize=(15, 15),
    #                  maxLevel=2,
    #                  criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    #
    # # Create some random colors
    # color = np.random.randint(0, 255, (100, 3))
    #
    # # Take first frame and find corners in it
    # ret, old_frame = cam.read()
    # old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    # p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    #
    # # Create a mask image for drawing purposes
    # mask = np.zeros_like(old_frame)

    while True:
        s, img = cam.read()
        # height, width, channels = img.shape
        # print(height, width, channels)
        if s:    # frame captured without any errors
            Analysis(img)
            # frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #
            # PotentialGoodNewPoints = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
            # for i in PotentialGoodNewPoints:
            #     if i not in p0 and p0.shape[0] < 15:
            #         print(np.array([i]))
            #         p0 = np.concatenate((p0, np.array([i])))
            #
            # # calculate optical flow
            # p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            #
            # # Select good points
            # good_new = p1[st == 1]
            # good_old = p0[st == 1]
            #
            # # draw the tracks
            # for i, (new, old) in enumerate(zip(good_new, good_old)):
            #     a, b = new.ravel()
            #     c, d = old.ravel()
            #     mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
            #     frame = cv2.circle(img, (a, b), 5, color[i].tolist(), -1)
            # img = cv2.add(img, mask)
            #
            # cv2.imshow('frame', img)
            # k = cv2.waitKey(30) & 0xff
            # if k == 27:
            #     break
            #
            # # Now update the previous frame and previous points
            # old_gray = frame_gray.copy()
            # p0 = good_new.reshape(-1, 1, 2)
            # namedWindow("cam-test")#,CV_WINDOW_AUTOSIZE)
            # imshow("cam-test",img)
            # waitKey(0)
            # destroyWindow("cam-test")
            # imwrite("filename.jpg",img) #save image
else:

    img = cv2.imread("filename.jpg")
    Analysis(img)


# cv2.imread()