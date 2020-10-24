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
TopLeftCriteria = "ABCDEFGH"

def FindCorners(img):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    VanishingPoint = []
    QrCodeImportantPoints = [[[10000,10000]],[[-10000,10000]],[[-10000,-10000]],[[10000,-10000]]] #[[TopLeft],[TopRight],[BottomRight],[BottomLeft]] points
    QrCodeImportantPointsLocationRealHorizontal = [0,0,0,0]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ArrayDecode = decode(gray)
    DataScanned = []
    for code in ArrayDecode:
        Data = code.data.decode('utf-8')
        # print(Data)
        DataScanned.append(Data) #Grab which barcodes were scanned
    for code in ArrayDecode:
        # Calculate where corners should be using each qrcode
        Data = code.data.decode('utf-8')
        pts = np.array([code.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))

        btmPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][1]))[2:4]
        topPts = np.array(sorted(pts.tolist(), key=lambda x: x[0][1]))[0:2]
        rightPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][0]))[2:4]
        leftPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][0]))[0:2]

        # print([topPts])
        cv2.polylines(img, [topPts], True, (0, 50, 50), 5)  # Color is bgr yellow
        cv2.polylines(img, [btmPts], True, (50, 0, 50), 5)  # Neon Purple
        cv2.polylines(img, [leftPts], True, (50, 50, 0), 5)  # Cyan
        cv2.polylines(img, [rightPts], True, (0, 0, 50), 5)  # Red
        TextPosition = np.average(pts, axis=0)[0] - (40, -40)
        cv2.putText(img, Data, tuple(TextPosition.astype(int)), font_face, 2, (50, 0, 50), 3, cv2.LINE_AA)

        topPts=topPts.sum(axis=1)
        btmPts=btmPts.sum(axis=1)

        TopRowExists = "A" in DataScanned or "B" in DataScanned or "C" in DataScanned
        BottomRowExists = "D" in DataScanned or "E" in DataScanned or "F" in DataScanned or "G" in DataScanned or "H" in DataScanned

        CurrentCodeinTopRow = (TopRowExists and Data in "ABC") or (not TopRowExists and Data in "DEFGH")
        CurrentCodeinBottomRow = ((BottomRowExists and Data in "DEFGH") or (not BottomRowExists and Data in "ABC")) and ( len(set(Data)&set("DEFGH")) >= 2 or topPts[0][1]-topPts[0][0] > 40)

        for pt in pts:
            if(math.dist([0,0],pt[0]) < math.dist([0,0],QrCodeImportantPoints[0][0]) and CurrentCodeinTopRow and pt in topPts): # TopLeft
                QrCodeImportantPoints[0]=pt
                QrCodeImportantPointsLocationRealHorizontal[0] = QRCodeLocation[Data][0]
            if(math.dist([700,0],pt[0]) < math.dist([700,0],QrCodeImportantPoints[1][0]) and CurrentCodeinTopRow and pt in topPts): # TopRight
                QrCodeImportantPoints[1] = pt
                QrCodeImportantPointsLocationRealHorizontal[1] = QRCodeLocation[Data][1]
            if (math.dist([700, 400], pt[0]) < math.dist([700, 400], QrCodeImportantPoints[2][0]) and CurrentCodeinBottomRow and pt in btmPts):  # BottomRight
                QrCodeImportantPoints[2] = pt
                QrCodeImportantPointsLocationRealHorizontal[2] = QRCodeLocation[Data][1]
            if (math.dist([0, 400], pt[0]) < math.dist([0, 400], QrCodeImportantPoints[3][0]) and CurrentCodeinBottomRow and pt in btmPts):  # BottomLeft
                QrCodeImportantPoints[3] = pt
                QrCodeImportantPointsLocationRealHorizontal[3] = QRCodeLocation[Data][0]
    if(DataScanned != []):
        #Calculate horizontal vanishing point
        xdiff = (QrCodeImportantPoints[0][0][0] - QrCodeImportantPoints[1][0][0], QrCodeImportantPoints[3][0][0] - QrCodeImportantPoints[2][0][0])
        ydiff = (QrCodeImportantPoints[0][0][1] - QrCodeImportantPoints[1][0][1], QrCodeImportantPoints[3][0][1] - QrCodeImportantPoints[2][0][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:  # Handle the case where the lines are parrell
            return(None,img)
            raise Exception('lines do not intersect')

        d = (det(*[QrCodeImportantPoints[0][0],QrCodeImportantPoints[1][0]]), det(*[QrCodeImportantPoints[3][0],QrCodeImportantPoints[2][0]]))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        VanishingPoint = [int(x), int(y)]

        #Calculate the pixel location of a point along the top left edge of the qrcode array using crosspoint
        A = QrCodeImportantPoints[1][0] #point furthest to the right
        B = QrCodeImportantPoints[0][0]

        AB = math.dist(A,B)
        BV = math.dist(B,VanishingPoint)
        AV = math.dist(A,VanishingPoint)
        BC_prime = QrCodeImportantPointsLocationRealHorizontal[0]
        AC_prime = QrCodeImportantPointsLocationRealHorizontal[1]

        if(BV*BC_prime-AV*AC_prime == 0): #Need to handle this case better in the future, im not sure what causes this but it happens every so often, so maby its random
            return
        BC=-(AB*BV*BC_prime)/(BV*BC_prime-AV*AC_prime)

        #Calculate the absolute edge location in pixels
        LeftTopEdgeLocation = [int(BC*np.dot((B-A),(1,0))/(AB)+B[0]),int(BC*np.dot((B-A),(0,1))/(AB)+B[1])]#int(BC*np.dot((B-A),(0,1))/(AB)+B[1])]

        #Calculate the pixel location of a point along the top right edge of the page using crosspoint
        BC = -(AB * AV * (QRSize[0]-AC_prime)) / (AV * (QRSize[0]-AC_prime) - BV * (QRSize[0]-BC_prime))
        RightTopEdgeLocaiton =  [int(BC*np.dot((A-B),(1,0))/(AB)+A[0]),int(BC*np.dot((A-B),(0,1))/(AB)+A[1])]

        #Calculate the pixel location of a point along the bottom left edge of the page using crosspoint
        A = QrCodeImportantPoints[2][0]  # point furthest to the right
        B = QrCodeImportantPoints[3][0]

        AB = math.dist(A, B)
        BV = math.dist(B, VanishingPoint)
        AV = math.dist(A, VanishingPoint)
        BC_prime = QrCodeImportantPointsLocationRealHorizontal[3]
        AC_prime = QrCodeImportantPointsLocationRealHorizontal[2]

        if (BV * BC_prime - AV * AC_prime == 0):  # Need to handle this case better in the future, im not sure what causes this but it happens every so often, so maby its random
            print("skippp")
            return(None,img)
        BC = -(AB * BV * BC_prime) / (BV * BC_prime - AV * AC_prime)

        # Calculate the absolute edge location in pixels
        LeftBtmEdgeLocation = [int(BC * np.dot((B - A), (1, 0)) / (AB) + B[0]), int(BC * np.dot((B - A), (0, 1)) / (AB) + B[1])]

        #Calculate the pixel location of a point along the bottom right edge of the page using crosspoint
        BC = -(AB * AV * (QRSize[0]-AC_prime)) / (AV * (QRSize[0]-AC_prime) - BV * (QRSize[0]-BC_prime))
        RightBtmEdgeLocaiton =  [int(BC*np.dot((A-B),(1,0))/(AB)+A[0]),int(BC*np.dot((A-B),(0,1))/(AB)+A[1])]

        QRArray = np.array([LeftTopEdgeLocation,RightTopEdgeLocaiton,RightBtmEdgeLocaiton,LeftBtmEdgeLocation])
        cv2.polylines(img, [QRArray], True, (0, 0, 255), 5)  # Red

        return([LeftTopEdgeLocation, RightTopEdgeLocaiton, RightBtmEdgeLocaiton, LeftBtmEdgeLocation],img)

    return(None,img)

if(fromCamera):
    cam = VideoCapture(0)

    while True:
        s, img = cam.read()
        if s:    # frame captured without any errors
            Corners,img = FindCorners(img)
            cv2.imshow("Result", img)
            cv2.waitKey(1)
else:

    img = cv2.imread("filename.png")
    Analysis(img)
    cv2.waitKey(0)

# cv2.imread()