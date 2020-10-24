import math
import numpy as np
from PIL import Image
# from ProbabilityCalculation.ProbabilityCalculation import ProbabilityCalculator as ProbabilityCalculator
import ProbabilityCalculation

Competiton_Zone_Width = 6
Competiton_Zone_Height = 6
Split = .05 #meters/cell
AngleSplit = 1 #Degrees/cell
Competiton_Zone_Width_Zones = int(Competiton_Zone_Width/Split)
Competiton_Zone_Height_Zones = int(Competiton_Zone_Height/Split)
Angle_Zones = int(360/AngleSplit)

LeftEncoder = 1.57/4
RightEncoder = -1.57/4
Width = .5

# ProbabilityZone_Old = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
ProbabilityZone_New2 = np.zeros((int(Competiton_Zone_Height_Zones),int(Competiton_Zone_Width_Zones),Angle_Zones))
# data = np.zeros((int(Competiton_Zone_Width_Zones),int(Competiton_Zone_Height_Zones),3),dtype=np.uint8)
# print(data[0,0,0])
# ProbabilityZone_Old[int(Competiton_Zone_Height_Zones/2),int(Competiton_Zone_Width_Zones/2),0]=1
# print(ProbabilityZone_Old[int(Competiton_Zone_Height_Zones)-1,int(Competiton_Zone_Width_Zones/2),0])
# img = Image.fromarray(data)
# img = img.resize((100*Competiton_Zone_Width,100*Competiton_Zone_Height),Image.NEAREST)
# img.show()

# imgdata = np.sum(ProbabilityZone_Old*255,2)
# img = Image.fromarray(imgdata)
# img = img.resize((100*Competiton_Zone_Width,100*Competiton_Zone_Height),Image.NEAREST)
# img.show()

# print(Competiton_Zone_Width_Zones)

import time
def Calculate(E1,E2,Prob_Zone_Old, Visuals = True):
    t_init = time.perf_counter()

    Const = 25
    max_prob = 0

    ProbabilityZone_New = np.zeros((int(Competiton_Zone_Height_Zones), int(Competiton_Zone_Width_Zones), Angle_Zones))
    for x_old in range(Competiton_Zone_Width_Zones):
        for y_old in range(Competiton_Zone_Height_Zones):
            for Angle_old in range(Angle_Zones-1):
                if(Prob_Zone_Old[y_old,x_old,Angle_old] < .01):
                    continue
                #Predict where the robot will end up exactly here, and only evaluate that range
                # print('Evaluation Probabilities for X:' + str(x_old*Split) + " Y:" + str(y_old*Split) + " A:" + str(Angle_old*AngleSplit))

                #Find the solution without any error:
                # if(E1 != E2):
                #     Radius_Exact = .5 * Width * (E1 + E2) / (E2 - E1)
                #     Rot_Exact = E1*360/(math.pi*Width*(1-(E1+E2)/(E2-E1)))
                #     X_Exact = -np.sign(Radius_Exact)*(abs(Radius_Exact) * math.sin(math.radians(Rot_Exact+90))-abs(Radius_Exact))+x_old*Split
                #     Y_Exact = abs(Radius_Exact)*math.cos(math.radians(Rot_Exact + 90))-y_old*Split
                #
                #     print(Radius_Exact)
                #     print(Rot_Exact)
                #
                # else:
                #     #Straight forward case
                #     print(math.sin(math.radians(Angle_old))*E1)
                #     print(math.cos(math.radians(Angle_old)))
                #     X_Exact = math.sin(math.radians(Angle_old))*E1+x_old*Split
                #     Y_Exact = math.cos(math.radians(Angle_old))*E1-y_old*Split

                # print([X_Exact, Y_Exact])

                for x_eval in range(Competiton_Zone_Width_Zones):
                    for y_eval in range(Competiton_Zone_Height_Zones):
                        # if(math.hypot(x_eval - x_old, y_eval - y_old) > Const * (E1+E2)/2):
                        #     continue

                        # if(math.sqrt((x_eval-x_old)**2 + (y_eval-y_old)**2) > (LeftEncoder + RightEncoder)):
                        #     continue
                        # print(str(x_eval * Split) + "   " + str(-y_eval * Split) + "   " + str(ProbabilityCalculator(x_old*Split,-y_old*Split,Angle_old*AngleSplit,x_eval*Split,-y_eval*Split,-57,LeftEncoder,RightEncoder,Width)))
                        #for Angle_eval in range(Angle_Zones - 1):
                        if(Visuals > 1):
                            print([x_old*Split,-y_old*Split,Angle_old*AngleSplit,x_eval*Split,-y_eval*Split,0*AngleSplit,E1,E2,Width])
                        [Prob, Angle] = ProbabilityCalculation.ProbabilityCalculator(x_old*Split,-y_old*Split,Angle_old*AngleSplit,x_eval*Split,-y_eval*Split,0*AngleSplit,E1,E2,Width)
                        max_prob = max(max_prob,Prob)
                        ProbabilityZone_New[y_eval,x_eval,math.floor(Angle/AngleSplit)] = ProbabilityZone_New[y_eval,x_eval,math.floor(Angle/AngleSplit)] + Prob*Prob_Zone_Old[y_old,x_old,Angle_old]

                # print(str(x_old) + " " + str(y_old) + " " + str(Angle_old))
    # print(time.perf_counter()-t_init)
    # print(np.max(ProbabilityZone_New))

    if(Visuals != 0):
        if(Visuals > 1):
            maxvaluehalved = np.max(ProbabilityZone_New)/5
            for x_old in range(Competiton_Zone_Width_Zones):
                for y_old in range(Competiton_Zone_Height_Zones):
                    for Angle_old in range(Angle_Zones-1):
                        if(ProbabilityZone_New[y_old, x_old, Angle_old] > maxvaluehalved):
                            print("Y:" + str(-y_old*Split) + " X:" + str(x_old*Split) + " A:" + str(Angle_old*AngleSplit) + " P:" +str(ProbabilityZone_New[y_old, x_old, Angle_old]))

        if(Visuals > 0):
            ProbabilityZone_New = ProbabilityZone_New*(1/np.max(ProbabilityZone_New))
            ProbabilityZone_New[int(Competiton_Zone_Height_Zones/2),int(Competiton_Zone_Width_Zones/2),0]=10
            imgdata = np.sum(ProbabilityZone_New*255,2)
            img = Image.fromarray(imgdata)
            img = img.resize((100*Competiton_Zone_Width,100*Competiton_Zone_Height),Image.NEAREST)
            img.show()

    return ProbabilityZone_New, max_prob

# Prob_Step_1 = Calculate(1,1,ProbabilityZone_Old)
# Prob_Step_2 = Calculate(-2,-2,Prob_Step_1)
# Prob_Step_2 = Calculate(2,2,Prob_Step_2)
# Prob_Step_2 = Calculate(-2,-2,Prob_Step_2)

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

# print(x)
# print(y)
# print(z)
# print(values)