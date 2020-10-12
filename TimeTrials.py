from FullStack import Calculate
import time
import numpy as np
import random

Trials = 1000

Competiton_Zone_Width = 6
Competiton_Zone_Height = 6
Split = .05 #meters/cell
AngleSplit = 1 #Degrees/cell
Competiton_Zone_Width_Zones = int(Competiton_Zone_Width/Split)
Competiton_Zone_Height_Zones = int(Competiton_Zone_Height/Split)
Angle_Zones = int(360/AngleSplit)

StartingMap = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
# StartingMap[int(Competiton_Zone_Height_Zones/2),int(Competiton_Zone_Width_Zones/2),0]=1

StartTime = time.perf_counter()
for i in range(Trials):
    RandomRotationStart = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
    E1_rand = random.uniform(-4,4)
    E2_rand = random.uniform(-4,4)
    Rotation_rand = random.randint(0,359)
    RandomRotationStart[int(Competiton_Zone_Height_Zones / 2), int(Competiton_Zone_Width_Zones / 2), Rotation_rand] = 1
    [Out1, Max_Prob] = Calculate(E1_rand, E2_rand, RandomRotationStart, Visuals=0)
    print([E1_rand,E2_rand,float(Rotation_rand), Max_Prob])
TrialTimes = (time.perf_counter()-StartTime)/Trials
print(TrialTimes)

# Notes:
# Initial: