from cv2 import *
import numpy as np
from pyzbar.pyzbar import decode,ZBarSymbol
import math
import statistics
import logging
logging.basicConfig(filename='ErrorLog.log',level=logging.DEBUG)

fromCamera = True
Calibrating = False

def Analysis(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for barcode in decode(gray):
        print(barcode)
        myData = barcode.data.decode('utf-8')
        pts=np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
    cv2.imshow("Result",img)
    cv2.waitKey(1)

QRSize = [1.00,.50] #Total qr code matrix size
QRCodeLocation = { #Matrix with the qr code data and the left/right/top/bottom side of the qr code position
    "A":[.013,.3158,.0135,.3158],
    "B":[.35,.65,.0135,.3158],
    "C":[.68,.98,.0135,.3158],
    "D":[.006,.162,.337,.49],
    "E":[.2134,.3658,.337,.49],
    "F":[.42,.575,.337,.49],
    "G":[.624,.78,.337,.49],
    "H":[.84,.994,.337,.49]
}
TopLeftCriteria = "ABCDEFGH"

#Camera resolution
X_Res = 640
Y_Res = 360
CameraViewAngle = 60
BoardWidth = 1 #Board Width in meters

def FindCorners(img):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    VanishingPoint = []
    QrCodeImportantPoints = [[[10000,10000]],[[-10000,10000]],[[-10000,-10000]],[[10000,-10000]]] #[[TopLeft],[TopRight],[BottomRight],[BottomLeft]] points
    QrCodeImportantPointsLocationRealHorizontal = [0,0,0,0]
    QrCodeImportantPointsLocationRealVertical = [0,0,0,0]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ArrayDecode = decode(gray)
    DataScanned = []

    ImageDimensions = img.shape
    X_Res = ImageDimensions[1]
    Y_Res = ImageDimensions[0]
    
    for code in ArrayDecode: # Determine what barcode lables were scanned
        Data = code.data.decode('utf-8')
        DataScanned.append(Data) #Grab which barcodes were scanned

    for code in ArrayDecode:
        # Calculate where corners should be using each qrcode
        Data = code.data.decode('utf-8')

        pts = np.array([code.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))

        #Split rectangles into line segments and categorize into top,bottom,left,and right
        #This fails if the board is rotated more than 45 degrees
        btmPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][1]))[2:4]
        topPts = np.array(sorted(pts.tolist(), key=lambda x: x[0][1]))[0:2]
        rightPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][0]))[2:4]
        leftPts = np.array(sorted(pts.tolist(),key=lambda x: x[0][0]))[0:2]

        #Draw boxes on the image around scanned barcodes, place text with data information ontop of them
        cv2.polylines(img, [topPts], True, (0, 50, 50), 5)  # Color is bgr yellow
        cv2.polylines(img, [btmPts], True, (50, 0, 50), 5)  # Neon Purple
        cv2.polylines(img, [leftPts], True, (50, 50, 0), 5)  # Cyan
        cv2.polylines(img, [rightPts], True, (0, 0, 50), 5)  # Red
        TextPosition = np.average(pts, axis=0)[0] - (40, -40)
        cv2.putText(img, Data, tuple(TextPosition.astype(int)), font_face, 2, (50, 0, 50), 3, cv2.LINE_AA)

        #Collapse wierd cv2 point information into something more usable
        topPts=topPts.sum(axis=1)
        btmPts=btmPts.sum(axis=1)

        # Is the resolution accurate enough to determine the board position using only the bottom barcodes
        IsBottomRowAccurateEnough = (len(set(DataScanned) & set("DEFGH")) >= 3 or (len(set(DataScanned) & set("DEFGH")) >= 1 and math.dist(topPts[1], topPts[0]) > 100)) #100 is the minimum height of the barcode in pix
        # Did one of the larger top barcodes get scanned
        TopRowExists = "A" in DataScanned or "B" in DataScanned or "C" in DataScanned
        # Does the bottom row exist, and is it accurate enough, or is it the only barcode scanned, if this is the case we will calculate using part or all of the bottom row
        BottomRowUsedInCalculation = ("D" in DataScanned or "E" in DataScanned or "F" in DataScanned or "G" in DataScanned or "H" in DataScanned) and (IsBottomRowAccurateEnough or TopRowExists == False)
        # Is the barcode that is being currently evaluated part of the top row
        CurrentCodeinTopRow = (TopRowExists and Data in "ABC") or (not TopRowExists and Data in "DEFGH")
        # Is the bottom row being used for calculation, and we are currently calculating the bottom row, or the bottom row is not and we need to calculate the bottom portion using the top row
        CurrentCodeinBottomRow = ((BottomRowUsedInCalculation and Data in "DEFGH") or (not BottomRowUsedInCalculation and Data in "ABC"))

        #Evaluate which points are closer to the edge of the board
        for pt in pts:
            if(math.dist([0,0],pt[0]) < math.dist([0,0],QrCodeImportantPoints[0][0]) and CurrentCodeinTopRow and pt in topPts): # TopLeft
                QrCodeImportantPoints[0]=pt
                QrCodeImportantPointsLocationRealHorizontal[0] = QRCodeLocation[Data][0]
                QrCodeImportantPointsLocationRealVertical[0] = QRCodeLocation[Data][2]
            if(math.dist([X_Res,0],pt[0]) < math.dist([X_Res,0],QrCodeImportantPoints[1][0]) and CurrentCodeinTopRow and pt in topPts): # TopRight
                QrCodeImportantPoints[1] = pt
                QrCodeImportantPointsLocationRealHorizontal[1] = QRCodeLocation[Data][1]
                QrCodeImportantPointsLocationRealVertical[1] = QRCodeLocation[Data][2]
            if (math.dist([X_Res, Y_Res], pt[0]) < math.dist([X_Res, Y_Res], QrCodeImportantPoints[2][0]) and CurrentCodeinBottomRow and pt in btmPts):  # BottomRight
                QrCodeImportantPoints[2] = pt
                QrCodeImportantPointsLocationRealHorizontal[2] = QRCodeLocation[Data][1]
                QrCodeImportantPointsLocationRealVertical[2] = QRCodeLocation[Data][3]
            if (math.dist([0, Y_Res], pt[0]) < math.dist([0, Y_Res], QrCodeImportantPoints[3][0]) and CurrentCodeinBottomRow and pt in btmPts):  # BottomLeft
                QrCodeImportantPoints[3] = pt
                QrCodeImportantPointsLocationRealHorizontal[3] = QRCodeLocation[Data][0]
                QrCodeImportantPointsLocationRealVertical[3] = QRCodeLocation[Data][3]
    if(QrCodeImportantPointsLocationRealVertical[2] != QrCodeImportantPointsLocationRealVertical[3]):
        print("BAd")
    if(DataScanned != []):
        # This ignores if duplicate points are in ImportantPoints
        Checker = []
        for Point in QrCodeImportantPoints:
            if(Point[0].tolist() in Checker):
                logging.error("Error, Duplicate points in QrCodeImportantPoints, QrCodeImportantPoints = {} pts = {}".format(QrCodeImportantPoints,pts))
                return None,None,None,None,None, img
            Checker.append(Point[0].tolist())

        ScanLeftSideEstimateReal = np.minimum(QrCodeImportantPointsLocationRealHorizontal[0],QrCodeImportantPointsLocationRealHorizontal[3])
        ScanRightSideEstimateReal = np.maximum(QrCodeImportantPointsLocationRealHorizontal[1],QrCodeImportantPointsLocationRealHorizontal[2])
        WidthOfScan = ScanRightSideEstimateReal-ScanLeftSideEstimateReal
        xPosOfLeftSideOfScan = ScanLeftSideEstimateReal
        HeightOfScan = -np.maximum(QrCodeImportantPointsLocationRealVertical[0],QrCodeImportantPointsLocationRealVertical[1])+np.minimum(QrCodeImportantPointsLocationRealVertical[2],QrCodeImportantPointsLocationRealVertical[3])

        #Calculate horizontal vanishing point
        xdiff = (QrCodeImportantPoints[0][0][0] - QrCodeImportantPoints[1][0][0], QrCodeImportantPoints[3][0][0] - QrCodeImportantPoints[2][0][0])
        ydiff = (QrCodeImportantPoints[0][0][1] - QrCodeImportantPoints[1][0][1], QrCodeImportantPoints[3][0][1] - QrCodeImportantPoints[2][0][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:  # Handle the case where the lines are parrell
            logging.warning("Error in Find Corners Vanishing Point Calculation, lines never cross, xdiff = {} ydiff = {} QrCodeImportantPoints = {}".format(xdiff,ydiff,QrCodeImportantPoints))
            VanishingPoint = [100000000000,statistics.mean(ydiff)*100000000000/statistics.mean(xdiff)]
        else:
            d = (det(*[QrCodeImportantPoints[0][0],QrCodeImportantPoints[1][0]]), det(*[QrCodeImportantPoints[3][0],QrCodeImportantPoints[2][0]]))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            VanishingPoint = [int(x), int(y)]

        #Calculate the pixel location of a point along the top left edge of the qrcode array using cross-ratio
        A = QrCodeImportantPoints[1][0] #point furthest to the right
        B = QrCodeImportantPoints[0][0] #point furthest to the left

        AB = math.dist(A,B)
        BV = math.dist(B,VanishingPoint)
        AV = math.dist(A,VanishingPoint)
        BC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[0] - ScanLeftSideEstimateReal)
        AC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[1] - ScanLeftSideEstimateReal)

        #issue caused when a point is not selected
        if(BV*BC_prime-AV*AC_prime == 0): #Need to handle this case better in the future, im not sure what causes this but it happens every so often, so maby its random
            logging.error("Error in Find Corners edge calculation 1, BV * BC_prime - AV * AC_prime == 0, BV = {} BC_prime = {} AV = {} AC_prime = {} A = {} B = {} VanishingPoint = {}".format(BV,BC_prime,AV,AC_prime,A,B,VanishingPoint))
            return (None,None,None,None,None, img)
        BC=-(AB*BV*(BC_prime))/(BV*(BC_prime)-AV*(AC_prime))

        #Calculate the absolute edge location in pixels
        LeftTopEdgeLocation = [int(BC*np.dot((B-A),(1,0))/(AB)+B[0]),int(BC*np.dot((B-A),(0,1))/(AB)+B[1])]

        BC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[0] - ScanRightSideEstimateReal)
        AC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[1] - ScanRightSideEstimateReal)

        #Calculate the pixel location of a point along the top right edge of the page using cross-ratio
        BC = -(AB * AV * (0-AC_prime)) / (AV * (0-AC_prime) - BV * (0-BC_prime))
        RightTopEdgeLocaiton =  [int(BC*np.dot((A-B),(1,0))/(AB)+A[0]),int(BC*np.dot((A-B),(0,1))/(AB)+A[1])]

        #Calculate the pixel location of a point along the bottom left edge of the page using crosspoint
        A = QrCodeImportantPoints[2][0]  # point furthest to the right
        B = QrCodeImportantPoints[3][0]

        AB = math.dist(A, B)
        BV = math.dist(B, VanishingPoint)
        AV = math.dist(A, VanishingPoint)
        BC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[3] - ScanLeftSideEstimateReal)
        AC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[2] - ScanLeftSideEstimateReal)

        if (BV * BC_prime - AV * AC_prime == 0):  # Need to handle this case better in the future, im not sure what causes this but it happens every so often, so maby its random
            logging.error("Error in Find Corners edge calculation 2, BV * BC_prime - AV * AC_prime == 0, BV = {} BC_prime = {} AV = {} AC_prime = {} A = {} B = {} VanishingPoint = {}".format(BV,BC_prime,AV,AC_prime,A,B,VanishingPoint))
            return (None,None,None,None,None, img)
        BC = -(AB * BV * BC_prime) / (BV * BC_prime - AV * AC_prime)

        # Calculate the absolute edge location in pixels
        LeftBtmEdgeLocation = [int(BC * np.dot((B - A), (1, 0)) / (AB) + B[0]), int(BC * np.dot((B - A), (0, 1)) / (AB) + B[1])]

        BC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[3] - ScanRightSideEstimateReal)
        AC_prime = abs(QrCodeImportantPointsLocationRealHorizontal[2] - ScanRightSideEstimateReal)

        #Calculate the pixel location of a point along the bottom right edge of the page using cross-ratio
        BC = -(AB * AV * (AC_prime)) / (AV * (AC_prime) - BV * (BC_prime))
        RightBtmEdgeLocaiton =  [int(BC*np.dot((A-B),(1,0))/(AB)+A[0]),int(BC*np.dot((A-B),(0,1))/(AB)+A[1])]

        QRArray = np.array([[LeftTopEdgeLocation, RightTopEdgeLocaiton, RightBtmEdgeLocaiton, LeftBtmEdgeLocation]])
        cv2.polylines(img, [QRArray], True, (0, 0, 255), 5)

        return([LeftTopEdgeLocation, RightTopEdgeLocaiton, RightBtmEdgeLocaiton, LeftBtmEdgeLocation],WidthOfScan,HeightOfScan,xPosOfLeftSideOfScan,VanishingPoint,img)

    return(None,None,None,None,None,img)

RefDistanceRight = 1 #Calibration distance in m
RefDistanceLeft = 1
RefrenceHeightRight = 500 #Calibration height in pix
RefrenceHeightLeft = 500

#Calibration for the position
x_CalibrationDelta = 1
x_CalibrationConstant = 0
y_CalibrationDelta = 1
y_CalibationConstant = 0

def GetDistance(Corners,WidthOfScannedSection,HeightOfScannedSection, LeftPositionOfScannedSection,VanishingPt,img = None,RefRenceDistance = RefDistanceRight, RefrenceHeight = RefrenceHeightRight):
    try:
        X_Res = img.shape[1]
    except:
        pass
    a = WidthOfScannedSection #Board Width in meters
    HeightMeasuredRightC = math.dist(Corners[2],Corners[1])*.5/HeightOfScannedSection #Vertical height of edge of board in pix
    HeightMeasuredLeftB = math.dist(Corners[0],Corners[3])*.5/HeightOfScannedSection

    if(Calibrating):
        logging.info("Calibration Height: Left = {}, Right = {}".format(HeightMeasuredLeftB,HeightMeasuredRightC))
        print("Calibration Height: Left = {}, Right = {}".format(HeightMeasuredLeftB,HeightMeasuredRightC))

    c = RefRenceDistance*RefrenceHeight/HeightMeasuredRightC #Distance from right side of board to camera
    b = RefRenceDistance*RefrenceHeight/HeightMeasuredLeftB #Distance from left side of board to camera

    try:
        ThetaB1 = math.acos((c**2-a**2-b**2)/(-2*a*b)) # Angle between board face and direction to camera, see notes for more info
    except:
        print("ThetaB1 Calculation Failure: " + str((c**2-a**2-b**2)/(-2*a*b)))
        logging.error("Failure Calculating ThetaB1, a,b,c cannot form a triangle " + "a = {} b = {} c = {} Corners = {}".format(a,b,c,Corners))
        return None,None,None

    y_rel = math.sin(ThetaB1)*b #Distance from left side of board to camera location
    x_rel = math.cos(ThetaB1)*b

    x_abs=x_rel+LeftPositionOfScannedSection-.5 #Distance from center of board to camera location
    y_abs=y_rel

    # Calculate rotation if qr code is centered in camera view
    a = -math.degrees(math.atan(x_abs / y_abs))

    # Calculate location of center of qr code
    B = np.array([int(statistics.mean([Corners[1][0],Corners[2][0]])),int(statistics.mean([Corners[1][1],Corners[2][1]]))])  # mean point right
    A = np.array([int(statistics.mean([Corners[0][0],Corners[3][0]])),int(statistics.mean([Corners[0][1],Corners[3][1]]))])  # mean point left

    AB = math.dist(A, B)
    BV = math.dist(B, VanishingPt)
    AV = math.dist(A, VanishingPt)
    AC_prime = abs(LeftPositionOfScannedSection - .5)
    BC_prime = abs(LeftPositionOfScannedSection + WidthOfScannedSection - .5)

    BC=abs((AB*BV*(BC_prime))/(BV*(BC_prime)+AV*(AC_prime)))

    CenterOfBarcodePoint = [int(-BC * np.dot((B - A), (1, 0)) / (AB) + B[0]),
                           int(-BC * np.dot((B - A), (0, 1)) / (AB) + B[1])]  # int(BC*np.dot((B-A),(0,1))/(AB)+B[1])]

    # Calculate deviation of center of qr code from the center of the camera's view
    b = (-CenterOfBarcodePoint[0] + X_Res / 2) * CameraViewAngle / X_Res

    cv2.circle(img,tuple(CenterOfBarcodePoint),5,(125,255,255),5)

    rotation = a + b

    return x_abs,y_abs,rotation

#x is the x position left and right from the center of the field
#y is the position away from the board
def displayPosition(x,y,angle):
    res = 100# 10cm is one pix
    angleDist = 10

    PosImg = np.zeros((6*res,2*res,3))
    x_pos = x*res+1*res
    y_pos = y*res
    cv2.circle(PosImg,(int(x_pos),int(y_pos)),5,(255,255,255))
    cv2.line(PosImg,(int(x_pos),int(y_pos)),(int(x_pos+math.sin(math.radians(angle))*angleDist),int(y_pos - math.cos(math.radians(angle))*angleDist)),(255,255,255))
    cv2.imshow("PositionImage",PosImg)

    return

if(__name__ == "__main__"):
    if(fromCamera):
        cam = VideoCapture(0)

        while True:
            s, img = cam.read()
            if s:    # frame captured without any errors
                Corners, WidthOfScan, HeightOfScan, xPosOfLeftSideOfScan, VanishingPoint, img = FindCorners(img)
                if Corners != None:
                    x, y, rot = GetDistance(Corners, WidthOfScan, HeightOfScan, xPosOfLeftSideOfScan,VanishingPoint, img)
                    if x != None:
                        displayPosition(x,y,rot)
                    print(x,y)
                cv2.imshow("Result", img)
                cv2.waitKey(1)
    else:

        img = cv2.imread("QRCodeBoard.png")
        Analysis(img)
        cv2.waitKey(0)
