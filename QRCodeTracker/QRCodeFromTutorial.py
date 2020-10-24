#https://www.youtube.com/watch?v=SrZuwM705yE&ab_channel=Murtaza%27sWorkshop-RoboticsandAI
# https://www.youtube.com/watch?v=dQrUilGMz_k&ab_channel=VipulVaibhaw

from cv2 import *
import numpy as np
from pyzbar.pyzbar import decode,ZBarSymbol
# import json
import math

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

QRSize = [100,50] #Total qr code matrix size
QRCodeLocation = { #Matrix with the qr code data and the left/right/top/bottom side of the qr code position
    "A":[1.3,31.58,1.35,31.58],
    "B":[35,65,1.35,31.58],
    "C":[68,98,1.35,31.58],
    "D":[.68,16.2,33.7,49],
    "E":[21.34,36.58,33.7,49],
    "F":[42,57.5,33.7,49],
    "G":[62.4,78,33.7,49],
    "H":[84,99.4,33.7,49]
}

def FindCorners(img):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    EdgeLocation = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for code in decode(gray):
        # Calculate where corners should be using each qrcode
        Data = code.data.decode('utf-8')
        pts = np.array([code.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))

        btmPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][1]))[2:4]
        topPts = np.array(sorted(pts.tolist(), key=lambda x: x[0][1]))[0:2]
        rightPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][0]))[2:4]
        leftPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][0]))[0:2]

        topPts=topPts.sum(axis=1)
        btmPts=btmPts.sum(axis=1)

        # Calculate the vanishing point by drawing a line from the top and bottom points and find where they intersect
        xdiff = (topPts[0][0] - topPts[1][0], btmPts[0][0] - btmPts[1][0])
        ydiff = (topPts[0][1] - topPts[1][1], btmPts[0][1] - btmPts[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:            #Handle the case where the lines are parrell
            continue
            raise Exception('lines do not intersect')

        d = (det(*topPts), det(*btmPts))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        VanishingPoint = (int(x),int(y))

        #Calculate the distance in pixels that the edge of the qrcode array is from each qr code using a modified cross-ratio equation
        topPts = np.array(sorted(topPts,key=lambda x: x[0]))
        B = topPts[0] #point furthest to the right
        A = topPts[1]

        AB = math.dist(A,B)
        BV = math.dist(B,VanishingPoint)
        AV = math.dist(A,VanishingPoint)
        BC_prime = QRCodeLocation[Data][0]
        AC_prime = QRCodeLocation[Data][1]

        BC=-(AB*BV*BC_prime)/(BV*BC_prime-AV*AC_prime)

        #Calculate the absolute edge location in pixels
        LeftEdgeLocation = [int(BC*np.dot((B-A),(1,0))/(AB)+B[0]),int(B[1])]#int(BC*np.dot((B-A),(0,1))/(AB)+B[1])]
        # EdgeLocation.append(LeftEdgeLocation)
        # print(B-A)


        #Render the Object
        cv2.polylines(img, [topPts], True, (0,255,255),5) #Color is bgr yellow
        cv2.polylines(img, [btmPts], True, (255, 0, 255), 5) # Neon Purple
        cv2.polylines(img, [leftPts], True, (255, 255, 0), 5) # Cyan
        cv2.polylines(img, [rightPts], True, (0, 0, 255), 5) # Red
        TextPosition = np.average(pts,axis=0)[0]-(40,-40)
        cv2.putText(img, Data, tuple(TextPosition.astype(int)), font_face, 2, (255,0,255), 3, cv2.LINE_AA)
        cv2.circle(img, tuple(LeftEdgeLocation), 3, (100, 100, 100), 5)
    # if(EdgeLocation != []):
    #     EdgeLocation = tuple(np.array(EdgeLocation).mean(axis=0).astype(int))
    #     cv2.circle(img,EdgeLocation,3,(100,100,100),5)
    cv2.imshow("Result", img)
    cv2.waitKey(1)

if(fromCamera):
    cam = VideoCapture(0)

    while True:
        s, img = cam.read()
        if s:    # frame captured without any errors
            FindCorners(img)
else:

    img = cv2.imread("filename.png")
    Analysis(img)
    cv2.waitKey(0)

# cv2.imread()