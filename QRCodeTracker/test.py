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
R_Values = np.array(np.concatenate((np.linspace(0,0,100),np.linspace(0,38.8,30),np.linspace(38.8,-39,30),np.linspace(-39,0,40),np.linspace(0,0,70))))

frame = 0

deviation = []

img = cv2.imread("QRCodeBoard12.png")

Corners,WidthOfScan,HeightOfScan,xPosOfLeftSideOfScan,VanishingPoint,img = QRCodeFromTutorial.FindCorners(img)
if Corners != None:
    x,y,rot = QRCodeFromTutorial.GetDistance(Corners,WidthOfScan,HeightOfScan, xPosOfLeftSideOfScan,VanishingPoint,img,RefRenceDistance=1.619,RefrenceHeight=872.82,h_fov = 40)

    # print(x,y,rot)
    if x != None:
        dev = [x-X_Values[frame],y-Y_Values[frame],rot-R_Values[frame]]
        print(dev)
        deviation.append(dev)
        QRCodeFromTutorial.displayPosition(x, y, rot)
    else:
        print("Error")

cv2.imshow("Result", img)
cv2.waitKey(0)

while(cap.isOpened()):

    ret, img = cap.read()
    if(ret == False):
        break

    Corners,WidthOfScan,HeightOfScan,xPosOfLeftSideOfScan,VanishingPoint,img = QRCodeFromTutorial.FindCorners(img)
    if Corners != None:
        x,y,rot = QRCodeFromTutorial.GetDistance(Corners,WidthOfScan,HeightOfScan, xPosOfLeftSideOfScan,VanishingPoint,img,RefRenceDistance=1.619,RefrenceHeight=872.82,h_fov = 40)

        # print(x,y,rot)
        if x != None:
            dev = [abs(x-X_Values[frame]),abs(y-Y_Values[frame]),abs(rot-R_Values[frame])]
            print(dev)
            deviation.append(dev)
            QRCodeFromTutorial.displayPosition(x, y, rot)
        else:
            print("Error")

    cv2.imshow("Result", img)
    cv2.waitKey(5)
    frame = frame + 1

xdev = [x[0] for x in deviation]
ydev = [y[1] for y in deviation]
rdev = [y[2] for y in deviation]

print("Xdev: {}, Xmax: {} meters".format(statistics.stdev(xdev),max(xdev)))
print("Ydev: {}, Ymax: {} meters".format(statistics.stdev(ydev),max(ydev)))
print("Rdev: {}, Rmax: {} degrees".format(statistics.stdev(rdev),max(rdev)))

