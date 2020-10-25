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
    QrCodeImportantPointsLocationRealVertical = [0,0,0,0]
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

        cv2.polylines(img, [topPts], True, (0, 50, 50), 5)  # Color is bgr yellow
        cv2.polylines(img, [btmPts], True, (50, 0, 50), 5)  # Neon Purple
        cv2.polylines(img, [leftPts], True, (50, 50, 0), 5)  # Cyan
        cv2.polylines(img, [rightPts], True, (0, 0, 50), 5)  # Red
        TextPosition = np.average(pts, axis=0)[0] - (40, -40)
        cv2.putText(img, Data, tuple(TextPosition.astype(int)), font_face, 2, (50, 0, 50), 3, cv2.LINE_AA)

        topPts=topPts.sum(axis=1)
        btmPts=btmPts.sum(axis=1)

        IsBottomRowAccurateEnough = (len(set(DataScanned) & set("DEFGH")) >= 3 or (Data in "DEFGH" and math.dist(topPts[1], topPts[0]) > 100))

        TopRowExists = "A" in DataScanned or "B" in DataScanned or "C" in DataScanned
        BottomRowExists = ("D" in DataScanned or "E" in DataScanned or "F" in DataScanned or "G" in DataScanned or "H" in DataScanned) and (IsBottomRowAccurateEnough or TopRowExists == False)

        CurrentCodeinTopRow = (TopRowExists and Data in "ABC") or (not TopRowExists and Data in "DEFGH")
        CurrentCodeinBottomRow = ((BottomRowExists and (IsBottomRowAccurateEnough or TopRowExists == False) and Data in "DEFGH") or (not BottomRowExists and Data in "ABC"))


        # print(DataScanned)
        # print("Data: " + str(Data))
        # print("Accurate: " + str(IsBottomRowAccurateEnough))
        # print(BottomRowExists)
        for pt in pts:
            # print("Current Code: " + str(CurrentCodeinBottomRow))
            # if(CurrentCodeinBottomRow and pt in btmPts):
                # print(math.dist([700, 400], pt[0]),math.dist([700, 400], QrCodeImportantPoints[2][0]))
            # print(np.sum(QrCodeImportantPoints,axis=1))

            if(math.dist([0,0],pt[0]) < math.dist([0,0],QrCodeImportantPoints[0][0]) and CurrentCodeinTopRow and pt in topPts): # TopLeft
                QrCodeImportantPoints[0]=pt
                QrCodeImportantPointsLocationRealHorizontal[0] = QRCodeLocation[Data][0]
                QrCodeImportantPointsLocationRealVertical[0] = QRCodeLocation[Data][2]
            if(math.dist([700,0],pt[0]) < math.dist([700,0],QrCodeImportantPoints[1][0]) and CurrentCodeinTopRow and pt in topPts): # TopRight
                QrCodeImportantPoints[1] = pt
                QrCodeImportantPointsLocationRealHorizontal[1] = QRCodeLocation[Data][1]
                QrCodeImportantPointsLocationRealVertical[1] = QRCodeLocation[Data][2]
            if (math.dist([700, 400], pt[0]) < math.dist([700, 400], QrCodeImportantPoints[2][0]) and CurrentCodeinBottomRow and pt in btmPts):  # BottomRight
                QrCodeImportantPoints[2] = pt
                QrCodeImportantPointsLocationRealHorizontal[2] = QRCodeLocation[Data][1]
                QrCodeImportantPointsLocationRealVertical[2] = QRCodeLocation[Data][3]
            if (math.dist([0, 400], pt[0]) < math.dist([0, 400], QrCodeImportantPoints[3][0]) and CurrentCodeinBottomRow and pt in btmPts):  # BottomLeft
                QrCodeImportantPoints[3] = pt
                QrCodeImportantPointsLocationRealHorizontal[3] = QRCodeLocation[Data][0]
                QrCodeImportantPointsLocationRealVertical[3] = QRCodeLocation[Data][3]
    if(QrCodeImportantPointsLocationRealVertical[2] != QrCodeImportantPointsLocationRealVertical[3]):
        print("BAd")
    if(DataScanned != []):
        # This ignores if duplicate points are in ImportantPoints
        Checker = []
        # print(QrCodeImportantPoints)
        for Point in QrCodeImportantPoints:
            # print("Checker: " + str(Checker))
            # print(Point[0])
            if(Point[0].tolist() in Checker):
                # print("Duplicate Point")
                return None, img
            Checker.append(Point[0].tolist())

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

        # if(VanishingPoint[0] > -300 and VanishingPoint[0] < 0):
        #     # print("Captured")
        #     return None, img

        #Calculate the pixel location of a point along the top left edge of the qrcode array using crosspoint
        A = QrCodeImportantPoints[1][0] #point furthest to the right
        B = QrCodeImportantPoints[0][0]

        AB = math.dist(A,B)
        BV = math.dist(B,VanishingPoint)
        AV = math.dist(A,VanishingPoint)
        BC_prime = QrCodeImportantPointsLocationRealHorizontal[0]
        AC_prime = QrCodeImportantPointsLocationRealHorizontal[1]

        #issue caused when a point is not selected
        if(BV*BC_prime-AV*AC_prime == 0): #Need to handle this case better in the future, im not sure what causes this but it happens every so often, so maby its random
            raise Exception('BV*BC_prime-AV*AC_prime == 0')
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
            raise Exception('BV*BC_prime-AV*AC_prime == 0')
        BC = -(AB * BV * BC_prime) / (BV * BC_prime - AV * AC_prime)

        # Calculate the absolute edge location in pixels
        LeftBtmEdgeLocation = [int(BC * np.dot((B - A), (1, 0)) / (AB) + B[0]), int(BC * np.dot((B - A), (0, 1)) / (AB) + B[1])]

        #Calculate the pixel location of a point along the bottom right edge of the page using crosspoint
        BC = -(AB * AV * (QRSize[0]-AC_prime)) / (AV * (QRSize[0]-AC_prime) - BV * (QRSize[0]-BC_prime))
        RightBtmEdgeLocaiton =  [int(BC*np.dot((A-B),(1,0))/(AB)+A[0]),int(BC*np.dot((A-B),(0,1))/(AB)+A[1])]

        # QRArray = np.array([LeftTopEdgeLocation,RightTopEdgeLocaiton,RightBtmEdgeLocaiton,LeftBtmEdgeLocation])
        # cv2.polylines(img, [QRArray], True, (0, 0, 255), 5)  # Red

        #Calculate the vanishing point for the edge lines
        # xdiff = (LeftTopEdgeLocation[0] - LeftBtmEdgeLocation[0],
        #          RightTopEdgeLocaiton[0] - RightBtmEdgeLocaiton[0])
        # ydiff = (LeftTopEdgeLocation[1] - LeftBtmEdgeLocation[1],
        #          RightTopEdgeLocaiton[1] - RightBtmEdgeLocaiton[1])
        #
        # d = (det(*[LeftTopEdgeLocation, LeftBtmEdgeLocation]),
        #      det(*[RightTopEdgeLocaiton, RightBtmEdgeLocaiton]))
        # x = det(d, xdiff) / div
        # y = det(d, ydiff) / div
        # VanishingPoint = [int(x), int(y)]
        # # print(VanishingPoint)
        #
        # # VanishingPoint = 10000
        #
        # # Calculate the pixel location of a point along the top left edge of the qrcode array using crosspoint
        # A = np.array(RightBtmEdgeLocaiton)  # bottom point left side
        # B = np.array(LeftTopEdgeLocation)  # top point left side
        #
        # AB = math.dist(A, B)
        # BV = math.dist(B, VanishingPoint)
        # AV = math.dist(A, VanishingPoint)
        # BC_prime = QrCodeImportantPointsLocationRealVertical[0]
        # AC_prime = QrCodeImportantPointsLocationRealVertical[3]
        #
        # # issue caused when a point is not selected
        # if (
        #         BV * BC_prime - AV * AC_prime == 0):  # Need to handle this case better in the future, im not sure what causes this but it happens every so often, so maby its random
        #     raise Exception('BV*BC_prime-AV*AC_prime == 0')
        # BC = -(AB * BV * BC_prime) / (BV * BC_prime - AV * AC_prime)
        #
        # # Calculate the absolute edge location in pixels
        # # print([LeftTopEdgeLocation, RightTopEdgeLocaiton, RightBtmEdgeLocaiton, LeftBtmEdgeLocation])
        # LeftTopEdgeLocationTrue = [int(BC * np.dot((B - A), (1, 0)) / (AB) + B[0]), int(
        #     BC * np.dot((B - A), (0, 1)) / (AB) + B[1])]  # int(BC*np.dot((B-A),(0,1))/(AB)+B[1])]
        # print(LeftTopEdgeLocationTrue,VanishingPoint)
        # cv2.circle(img, tuple(LeftTopEdgeLocationTrue),5,(255,0,255),5)

        #Calculate pixel/cm for each side
        LeftSideConversionY = (LeftBtmEdgeLocation[1]-LeftTopEdgeLocation[1])/(QrCodeImportantPointsLocationRealVertical[3]-QrCodeImportantPointsLocationRealVertical[0])
        RightSideConversionY = (RightBtmEdgeLocaiton[1]-RightTopEdgeLocaiton[1])/(QrCodeImportantPointsLocationRealVertical[2]-QrCodeImportantPointsLocationRealVertical[1])
        #Adjust the sides by the correct ammount
        Dy = -LeftSideConversionY*QrCodeImportantPointsLocationRealVertical[0]
        Dx = ((LeftBtmEdgeLocation[0]-LeftTopEdgeLocation[0])*Dy)/(LeftBtmEdgeLocation[1]-LeftTopEdgeLocation[1])
        LeftTopAdjusted = [int(Dx+LeftTopEdgeLocation[0]),
                           int(Dy+LeftTopEdgeLocation[1])]

        Dy = -LeftSideConversionY * (QrCodeImportantPointsLocationRealVertical[3]-QRSize[1])
        Dx = ((LeftBtmEdgeLocation[0] - LeftTopEdgeLocation[0]) * Dy) / (
                    LeftBtmEdgeLocation[1] - LeftTopEdgeLocation[1])
        LeftBtmAdjusted = [int(Dx + LeftBtmEdgeLocation[0]),int(Dy + LeftBtmEdgeLocation[1])]

        Dy = -RightSideConversionY * (QrCodeImportantPointsLocationRealVertical[1])
        Dx = ((RightBtmEdgeLocaiton[0] - RightTopEdgeLocaiton[0]) * Dy) / (
                RightBtmEdgeLocaiton[1] - RightTopEdgeLocaiton[1])
        RightTopAdjusted = [int(Dx + RightTopEdgeLocaiton[0]), int(Dy + RightTopEdgeLocaiton[1])]

        Dy = -RightSideConversionY * (QrCodeImportantPointsLocationRealVertical[2]-QRSize[1])
        Dx = ((RightBtmEdgeLocaiton[0] - RightTopEdgeLocaiton[0]) * Dy) / (
                RightBtmEdgeLocaiton[1] - RightTopEdgeLocaiton[1])
        RightBtmAdjusted = [int(Dx + RightBtmEdgeLocaiton[0]), int(Dy + RightBtmEdgeLocaiton[1])]

        # cv2.circle(img,tuple(LeftTopAdjusted),5,(255,255,0),5)

        QRArray = np.array([LeftTopAdjusted, RightTopAdjusted, RightBtmAdjusted, LeftBtmAdjusted])
        cv2.polylines(img, [QRArray], True, (0, 0, 255), 5)

        return([LeftTopAdjusted, RightTopAdjusted, RightBtmAdjusted, LeftBtmAdjusted],img)

    return(None,img)

RefDistanceRight = 0.5 #Calibration distance in m
RefDistanceLeft = 0.5
RefrenceHeightRight = 200 #Calibration height in pix
RefrenceHeightLeft = 200

def GetDistance(Corners):
    a = .5 #Board Width in meters
    HeightMeasuredRightC = abs(Corners[2][1] - Corners[1][1])
    HeightMeasuredLeftB = abs(Corners[0][1] - Corners[3][1])

    c = RefDistanceRight*RefrenceHeightRight/HeightMeasuredRightC
    b = RefDistanceLeft*RefrenceHeightLeft/HeightMeasuredLeftB

    ThetaB1 = math.acos((c**2-a**2-b**2)/(-2*a*b))

    y_rel = math.sin(ThetaB1)*b
    x_rel = math.cos(ThetaB1)*b

    x_abs=-.5/2+x_rel
    y_abs=y_rel

    return x_abs,y_abs

if(fromCamera):
    cam = VideoCapture(0)

    while True:
        s, img = cam.read()
        if s:    # frame captured without any errors
            Corners,img = FindCorners(img)
            if Corners != None:
                x,y = GetDistance(Corners)
                print(x,y)
            cv2.imshow("Result", img)
            cv2.waitKey(1)
else:

    img = cv2.imread("filename.png")
    Analysis(img)
    cv2.waitKey(0)

# cv2.imread()