from ProbabilityCalculation.FullStack import Calculate
import time
import numpy as np
import random
import math

Trials = math.floor(360/20)

Competiton_Zone_Width = 6
Competiton_Zone_Height = 6
Split = .05 #meters/cell
AngleSplit = 1 #Degrees/cell
Competiton_Zone_Width_Zones = int(Competiton_Zone_Width/Split)
Competiton_Zone_Height_Zones = int(Competiton_Zone_Height/Split)
Angle_Zones = int(360/AngleSplit)

StartingMap = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
# StartingMap[int(Competiton_Zone_Height_Zones/2),int(Competiton_Zone_Width_Zones/2),0]=1

IssuesList = []

Test = 5

StartTime = time.perf_counter()
for i in range(Trials):
    RandomRotationStart = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
    E1_rand = [1, 1.5,-1,-1.5,-0.6579586383468483,random.uniform(-2.5,2.5)]#
    E2_rand = [1, 1,-1,-1,-2.317075426677441,random.uniform(-2.5,2.5)]#random.uniform(-4,4)
    Rotation_rand = [math.floor(i*20),math.floor(i*20),math.floor(i*20),math.floor(i*20),math.floor(i*20),0]#math.floor(i*20)#random.randint(0,359)
    RandomRotationStart[int(Competiton_Zone_Height_Zones / 2), int(Competiton_Zone_Width_Zones / 2), Rotation_rand[Test]] = 1
    [Out1, Max_Prob] = Calculate(E1_rand[Test], E2_rand[Test], RandomRotationStart, Visuals=1)
    print([E1_rand[Test],E2_rand[Test],float(Rotation_rand[Test]), Max_Prob])
    if(Max_Prob < 1):
        IssuesList.append([E1_rand[Test],E2_rand[Test],float(Rotation_rand[Test]), Max_Prob])
TrialTimes = (time.perf_counter()-StartTime)/Trials
print(TrialTimes)
print(IssuesList)

# Notes:
# Initial: 1.6755