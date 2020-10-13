import math
import numpy as np
from PIL import Image

def ProbabilityCalculator(X_Start,Y_Start,Angle_Start,X_Box,Y_Box,Angle_Box,E1,E2,Robot_Width, Visuals = False):
    #Angle is measured in degrees from vertical between -180 and 180
    #E1 must be the left side encoder, and E2 must be the right side encoder

    if(Angle_Box > 180):
        Angle_Box = Angle_Box-360

    Sigma_E1 = .2 #Meters
    Sigma_E2 = .2 #Meters
    Sigma_Rot = 2 #Degrees

    Angle_Start_rad = math.radians(Angle_Start)
    Rad_180=math.radians(90)

    x_rot = (X_Box - X_Start) * math.cos(Angle_Start_rad) - (Y_Box - Y_Start) * math.sin(Angle_Start_rad)
    y_rot = (X_Box - X_Start) * math.sin(Angle_Start_rad) + (Y_Box - Y_Start) * math.cos(Angle_Start_rad)

    if(Visuals):
        print("X_Rot: " + str(x_rot))
        print("Y_Rot: " + str(y_rot))

    #Calculate R
    if((X_Box-X_Start) == 0 and (Y_Box-Y_Start) == 0):
        if(Visuals):
            print("Robot In Place Turning")
        #Case where robot turns in place
        #This is probably the place where the robot is most prone to error from slipping
        Angle_Delta = (((E1+E2)/2)*360)/(2*math.pi*Robot_Width/2)
        # print(Angle_Delta)
        TurningDirection = np.sign(E1)

        if(Visuals):
            print("Angle Delta: " + str(Angle_Delta))
        E1_Error = E1 + TurningDirection * 2 * math.pi * (- TurningDirection * Robot_Width / 2) * (Angle_Delta / 360)
        E2_Error = E2 + TurningDirection * 2 * math.pi * (+ TurningDirection * Robot_Width / 2) * (Angle_Delta / 360)

    elif(abs(x_rot) < .00001):
        if(Visuals):
            print("Robot Drives Straight")
        # R is infinite, and robot is attempting to drive straight forward
        Angle_Delta = 0
        # Distance = math.sqrt((X_Box-X_Start)**2+(Y_Box-Y_Start)**2)
        # E1_Error = E1 - Distance
        # E2_Error = E2 - Distance

        DriveDistance_y = np.sign(y_rot)*math.sqrt((X_Box-X_Start)**2+(Y_Box-Y_Start)**2)
        if(Visuals):
            print("Drive Distance: " + str(DriveDistance_y))

        E1_Error = E1-DriveDistance_y
        E2_Error = E2-DriveDistance_y

        # print('hi')
    else:
        if(Visuals):
            print("Robot Complex Turning")
        # Calculate turning direction, -1 is left, 1 is right

        # print('hi2')

        # print(x_rot)
        # print(y_rot)

        #Robot turns some ammount
        Axis_norm = 1 / math.sqrt((X_Box - X_Start) ** 2 + (Y_Box - Y_Start) ** 2)
        R=abs(x_rot/(2*(x_rot*Axis_norm*math.sin(Rad_180)
                                                            +y_rot*Axis_norm*math.cos(Rad_180))*x_rot*Axis_norm))

        # V_o_x = 2*Axis_norm*((X_Box-X_Start)*math.sin(Angle_Start_rad+Rad_180)+(Y_Box-Y_Start)*(math.cos(Angle_Start_rad+Rad_180)))*Axis_norm*(X_Box-X_Start)-math.sin(Angle_Start_rad+Rad_180)
        # V_o_y = 2 * Axis_norm * ((X_Box - X_Start) * math.sin(Angle_Start_rad + Rad_180) + (Y_Box - Y_Start) * (
        #     math.cos(Angle_Start_rad + Rad_180))) * Axis_norm * (Y_Box - Y_Start) - math.cos(Angle_Start_rad + Rad_180)





        if(y_rot != 0):
            TurningDirection = math.degrees(math.atan(x_rot/y_rot))
            # print(TurningDirection)
        elif(x_rot != 0):
            TurningDirection = 90-math.degrees(math.atan(y_rot/x_rot))
            # print(TurningDirection)



        # elif(x_rot > 0):
        #     TurningDirection = 90
        # else:
        #     TurningDirection = -90

        # print(TurningDirection)

        if(y_rot < 0):
            TurningDirection = TurningDirection + 180
        if(TurningDirection > 180):
            TurningDirection = TurningDirection - 360
        if(E1<0 and E2<0):
            TurningDirection = -TurningDirection


        #Fix this broken shit Angle_Delta calculation dosen't work at all
        # if(y_rot == 0):
        #     y_rot = .0001
        # Angle_Delta = -(math.degrees(math.atan(((-x_rot-R)/-y_rot)))+90)

        # print(x_rot)
        # print(y_rot)
        if(Visuals):
            print("Radius: " + str(R))


        TurningDirection = np.sign(TurningDirection)

        if(E1 < 0 and E2 < 0 and E1 > E2):
            TurningDirection = -TurningDirection # Case where backing up to the left
        elif(E1 < 0 and E2 < 0 and E1 < E2):
            TurningDirection = -TurningDirection # Case where backing up to the right

        # if(y_rot == 0 and abs(E1) > abs(E2)):
        #     TurningDirection = np.sign(E1)
        # elif(y_rot == 0 and abs(E1) < abs (E2)):
        #     print('hi')
        #     TurningDirection = -np.sign(E2)

        if(Visuals):
            print("Turning Direction: " + str(TurningDirection))

        # Fix this broken shit Angle_Delta calculation dosen't work at all
        # Angle_Delta = TurningDirection * ((E1 + E2) / 2) * 360 / (2 * math.pi * R)
        # print(Angle_Delta)

        # CircleCenter_x = TurningDirection*abs(R)
        #CircleCenterX cannot be based off the turning direction
        CircleCenter_x = abs(R)*np.sign(x_rot)
        if(Visuals):
            print("Circle Center x: " + str(CircleCenter_x))
        # print(x_rot)
        # print(y_rot)

        if(E1 ==E2 and E2 < 0):
            Backing = -1
        else:
            Backing = 1

        # print(R)
        #Turning Left
        if((TurningDirection*Backing == -1)):
            if (CircleCenter_x < x_rot and y_rot >= 0 and abs(x_rot) != R):
                Angle_Delta = -math.degrees(math.atan(abs(y_rot) / (-abs(x_rot) + R)))
                if (Visuals): print("Case 1")
            elif (CircleCenter_x <= x_rot and y_rot > 0):
                Angle_Delta = -90 + math.degrees(math.atan((-abs(x_rot) + R) / abs(y_rot)))
                if (Visuals): print("Case 2")
            elif (CircleCenter_x >= x_rot and y_rot > 0):
                Angle_Delta = -math.degrees(math.atan((abs(x_rot) - R) / abs(y_rot))) - 90
                if (Visuals): print("Case 3")
            elif (CircleCenter_x > x_rot and y_rot <= 0 and abs(x_rot) != R):
                Angle_Delta = -math.degrees(math.atan(abs(y_rot) / (abs(x_rot) - R))) - 180
                if (Visuals): print("Case 4")
            elif (CircleCenter_x >= x_rot and y_rot < 0):
                Angle_Delta = -90 + math.degrees(math.atan((abs(x_rot) - R) / abs(y_rot))) - 180
                if (Visuals): print("Case 5")
            elif (CircleCenter_x <= x_rot and y_rot < 0):
                Angle_Delta = -math.degrees(math.atan((R - abs(x_rot)) / abs(y_rot))) - 270
                if (Visuals): print("Case 6")
        elif((TurningDirection*Backing == 1)):
            if (CircleCenter_x > x_rot and y_rot >= 0 and abs(x_rot) != R):
                Angle_Delta = math.degrees(math.atan(abs(y_rot) / (-abs(x_rot) + R)))
                if (Visuals): print("Case 7")
            elif (CircleCenter_x >= x_rot and y_rot > 0):
                Angle_Delta = 90 - math.degrees(math.atan((-abs(x_rot) + R) / abs(y_rot)))
                if (Visuals): print("Case 8")
            elif (CircleCenter_x <= x_rot and y_rot > 0):
                Angle_Delta = math.degrees(math.atan((abs(x_rot) - R) / abs(y_rot))) + 90
                if (Visuals): print("Case 9")
            elif (CircleCenter_x < x_rot and y_rot <= 0 and abs(x_rot) != R):
                Angle_Delta = math.degrees(math.atan(abs(y_rot) / (abs(x_rot) - R))) + 180
                if (Visuals): print("Case 10")
            elif (CircleCenter_x <= x_rot and y_rot < 0):
                Angle_Delta = 90 - math.degrees(math.atan( (abs(x_rot) - R)/ abs(y_rot))) + 180
                if (Visuals): print("Case 11")
            elif (CircleCenter_x >= x_rot and y_rot < 0):
                Angle_Delta = math.degrees(math.atan((R - abs(x_rot)) / abs(y_rot))) + 270
                if (Visuals): print("Case 12")

        if(E1 < 0 and E2 < 0):
            Angle_Delta = TurningDirection*(abs(Angle_Delta) - 360)
        if(y_rot == 0): #Either Angle_Delta = either 180 or -180
            Angle_Delta = 180*TurningDirection
        if(y_rot == 0):
            Angle_Delta = -Angle_Delta

        if(Visuals):
            print("Angle Delta: " + str(Angle_Delta))

        # Circles= abs(E1/(math.pi*Robot_Width*(1-(E1+E2)/(E2-E1))))
        # CircleLeftover = Circles-math.floor(Circles)
        # WholeCircles = math.floor(Circles)
        # if(Visuals):
        #     print("Circles: " + str(Circles))
        #     print("Whole Circles: " + str(WholeCircles))
        #     print("Circle Leftovers: " + str(CircleLeftover))

        # DistanceDriven1 = np.sign(Angle_Delta)*Circles*TurningDirection*2*math.pi*(R+TurningDirection*Robot_Width/2)#*(Angle_Delta)/360
        # DistanceDriven2 = np.sign(Angle_Delta)*Circles*TurningDirection*2 * math.pi * (R - TurningDirection*Robot_Width / 2)# * (Angle_Delta / 360)

        if(CircleCenter_x < 0):
            InsideWheel = 1
            if(Visuals):
                print("Leftside is inside wheel")
        else:
            InsideWheel = -1
            if(Visuals):
                print("Rightside is inside wheel")

        DistanceDriven1 = 2*TurningDirection*math.pi*(R-InsideWheel*Robot_Width/2)*(Angle_Delta)/360#,abs(E1-TurningDirection*2*math.pi*(R+TurningDirection*Robot_Width/2)*(Angle_Delta-360)/360))
        DistanceDriven2 = 2*TurningDirection * math.pi * (R + InsideWheel*Robot_Width / 2) * (Angle_Delta / 360)#,abs(E2-TurningDirection*2 * math.pi * (R - TurningDirection*Robot_Width / 2) * (Angle_Delta-360) / 360))

        E1_Error = abs(E1-DistanceDriven1)#,abs(E1-TurningDirection*2*math.pi*(R+TurningDirection*Robot_Width/2)*(Angle_Delta-360)/360))
        E2_Error = abs(E2-DistanceDriven2)#,abs(E2-TurningDirection*2 * math.pi * (R - TurningDirection*Robot_Width / 2) * (Angle_Delta-360) / 360))

    # print(abs(E1-TurningDirection*2*math.pi*(R+TurningDirection*Robot_Width/2)*(Angle_Delta-360)/360))
    # print(TurningDirection*2 * math.pi * (R - TurningDirection*Robot_Width / 2) * (Angle_Delta / 360))
    if(Visuals):
        try:
            print("Distance Driven 1: " + str(DistanceDriven1))
        except:
            pass
        try:
            print("Distance Driven 2: " + str(DistanceDriven2))
        except:
            pass
        print("Error E1: " + str(E1_Error))
        print("Error E2: " + str(E2_Error))

    # Rot_Error = Angle_Delta+Angle_Start
    if(Visuals):
        # print("Rot Error: " + str(Rot_Error))
        print("Angle Delta: " + str(Angle_Delta))
    # print(Angle_Box)

    # print(E2_Error)
    Prob_E1_Error = (1 / (Sigma_E1 * math.sqrt(2 * math.pi))) * math.exp(-((E1_Error) ** 2) / (2 * Sigma_E1 ** 2))
    Prob_E2_Error = (1 / (Sigma_E2 * math.sqrt(2 * math.pi))) * math.exp(-((E2_Error) ** 2) / (2 * Sigma_E2 ** 2))
    #Prob_Rot = (1 / (Sigma_Rot * math.sqrt(2 * math.pi))) * math.exp(-((Rot_Error) ** 2) / (2 * Sigma_Rot ** 2))

    # print("Prob E1: " + str(Prob_E1_Error))
    # print("Prob E2: " + str(Prob_E2_Error))
    # print("Prob Rot: " + str(Prob_Rot))

    # if(Angle_Delta < 0 and E1 + E1_Error < E2 + E2_Error):
    #     Prob_Rot = 0
    # elif(Angle_Delta > 0 and E1 + E1_Error > E2 + E2_Error):
    #     Prob_Rot = 0
    # else:
    #     Prob_Rot = 1

    Probability = Prob_E1_Error * Prob_E2_Error# * Prob_Rot
    EndTurn = Angle_Delta+Angle_Start

    EndTurn = EndTurn - 360*math.floor(EndTurn/360)
    if(EndTurn == 360):
        EndTurn = 0

    return [Probability,EndTurn]

# print(ProbabilityCalculator(0,0,0,2,2,90,3.57,2.74,.5))

