import QRCodeFromTutorial
import cv2
import numpy as np
import statistics

p = 100
# Corners,WidthOfScannedSection, LeftPositionOfScannedSection
# Corners,WidthOfScan,HeightOfScan,xPosOfLeftSideOfScan,img = QRCodeFromTutorial.GetDistance([[0, 0], [p, 0], [p, p], [0, p]],1,0)

cap = cv2.VideoCapture('QrCodeTestVideo.avi')

Y_Values = np.array(np.concatenate((np.linspace(1.54,6,60),np.linspace(6,6,40),np.linspace(6,1,30),np.linspace(1,1,30),np.linspace(1,6,30),np.linspace(6,.363,40),np.linspace(.363,.363,40))))
X_Values = np.array(np.concatenate((np.linspace(0,0,60),np.linspace(0,-1,40),np.linspace(-1,-1,30),np.linspace(-1,1,30),np.linspace(1,1,30),np.linspace(1,0,10),np.linspace(0,0,30),np.linspace(0,-.444,20),np.linspace(-.444,.469,20))))

print(X_Values)

frame = 0

deviation = []

while(cap.isOpened()):

    ret, img = cap.read()
    if(ret == False):
        break

    Corners,WidthOfScan,HeightOfScan,xPosOfLeftSideOfScan,VanishingPoint,img = QRCodeFromTutorial.FindCorners(img)
    if Corners != None:
        x,y,rot = QRCodeFromTutorial.GetDistance(Corners,WidthOfScan,HeightOfScan, xPosOfLeftSideOfScan,VanishingPoint,img,RefRenceDistance=1.619,RefrenceHeight=872.82)

        # print(x,y,rot)
        if x != None:
            deviation.append([x-X_Values[frame],y-Y_Values[frame]])
            QRCodeFromTutorial.displayPosition(x, y, rot)
        else:
            print("Error")
        print(x,y,X_Values[frame],Y_Values[frame])

    cv2.imshow("Result", img)
    cv2.waitKey(5)
    frame = frame + 1

xdev = [x[0] for x in deviation]
ydev = [y[1] for y in deviation]

print("Xdev: {} meters".format(statistics.stdev(xdev)))
print("Ydev: {} meters".format(statistics.stdev(ydev)))