import math
import numpy as np
from ProbabilityCalculation.FullStack import Calculate

LeftEncoder = 0.3614229191491658
RightEncoder = -3.1778141147697676
Width = .5

Radius = -.5*Width*(LeftEncoder+RightEncoder)/(RightEncoder-LeftEncoder)
Rot = LeftEncoder*360/(math.pi*Width*(1-(LeftEncoder+RightEncoder)/(RightEncoder-LeftEncoder)))

print(Radius)
print(Rot)

# X = -(Radius*math.sin(math.radians(Rot+90))-Radius)
# Y = -Radius*math.cos(math.radians(Rot+90))

# print(1.5+X)
# print(-5.9+Y)

# print(ProbabilityCalculator(1.5,-5.9,0,1.5+X,-5.9+Y,Rot,LeftEncoder,RightEncoder,Width))
# print(ProbabilityCalculator(1.5,-6/2,0,1.5,-2.7,0,LeftEncoder,RightEncoder,Width))
# t_init = time.perf_counter()
# [Prob,Angle] = ProbabilityCalculator(1.5, -3.0, 0, 1.9500000000000002, -3.35, 0, -1.1, -1, 0.5)
# print(time.perf_counter()-t_init)
#
# print(Prob)
# print(Angle)
# print(ProbabilityCalculator(1.5,5.9,0,1.5,5.3,0,.5,2,Width))
Count = 0

Competiton_Zone_Width = 6
Competiton_Zone_Height = 6
Split = .05 #meters/cell
AngleSplit = 1 #Degrees/cell
Competiton_Zone_Width_Zones = int(Competiton_Zone_Width/Split)
Competiton_Zone_Height_Zones = int(Competiton_Zone_Height/Split)
Angle_Zones = int(360/AngleSplit)

Issues = [[-1, -1, 0.0, 3.978873577297384]]

StartingMap = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
StartingMap[int(Competiton_Zone_Height_Zones/2),int(Competiton_Zone_Width_Zones/2),int(Issues[Count][2])]=1

[ProbabilityZone_New, max_prob] = Calculate(2.5,3,StartingMap, Visuals = 1)
# Calculate(Issues[0][0],Issues[0][1],StartingMap, Visuals = 2)
# Y:-3.0500000000000003 X:3.0 A:314 P:2.522088074496643e-122
# x = []
# y = []
# z = []
# values = []
# #
# # # print(ProbabilityZone_New[int(.9/Split),int(2/Split),11])
# #
# Fig = True
# if(Fig == True):
#     for x_old in range(Competiton_Zone_Width_Zones):
#         for y_old in range(Competiton_Zone_Height_Zones):
#             for Angle_old in range(Angle_Zones-1):
#                 Prob = ProbabilityZone_New[y_old,x_old,Angle_old]
#                 x.append(x_old*Split)
#                 y.append(y_old*Split)
#                 z.append(Angle_old*AngleSplit)
#                 values.append(Prob)
#
#     fig = go.Figure(data=go.Volume(
#         x=x,
#         y=y,
#         z=z,
#         value=values,
#         isomin=0.1,
#         isomax=0.8,
#         opacity=0.1, # needs to be small to see through all surfaces
#         surface_count=17, # needs to be a large number for good volume rendering
#         ))
#     fig.show()
# [prob,turn] = ProbabilityCalculator(3.0, -3.0, 0, 3.1, -2.0, 0, 1, 1, 0.5, Visuals=True)
# [prob,turn] = ProbabilityCalculator(3.0, -3.0, 0, 3.05, -4.0, 0, -1, -1, 0.5, Visuals=True)
# print("Probability: " + str(prob))

# CircleCenter_x = .5
# R = .5
# for i in range(0,360):
#     x_rot = -math.cos(math.radians(i))*R+R
#     y_rot = math.sin(math.radians(i))*R
#     if (CircleCenter_x >= x_rot and y_rot >= 0):
#         Angle_Delta = math.degrees(math.atan(abs(y_rot) / (-abs(x_rot) + R)))
#     elif (CircleCenter_x <= x_rot and y_rot >= 0):
#         Angle_Delta = math.degrees(math.atan((abs(x_rot) - R) / abs(y_rot))) + 90
#     elif (CircleCenter_x <= x_rot and y_rot <= 0):
#         Angle_Delta = math.degrees(math.atan(abs(y_rot) / (abs(x_rot) - R))) + 180
#     elif (CircleCenter_x >= x_rot and y_rot <= 0):
#         Angle_Delta = math.degrees(math.atan((R - abs(x_rot)) / abs(y_rot))) + 270
#     print(str(i) + " " + str(Angle_Delta) + " " + str(x_rot) + " " + str(y_rot))