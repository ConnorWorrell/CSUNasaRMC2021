# CSU NASA RMC 2021

## Competition Info

Colorado State University competes in a [NASA hosted competition called Lunabotics](https://www.nasa.gov/offices/education/centers/kennedy/technology/nasarmc.html). This year the team consists of 9 main members, and supplemental help from [CSU's Ram Robotics club](https://www.engr.colostate.edu/organizations/robotics/ram_robotics/). CSU has competed in this competition since 2018.

| Year    | Info                                      |
| ------- | ----------------------------------------- |
| 2018-19 |                                           |
| 2019-20 |                                           |
| 2020-21 | [GitHub](https://github.com/CSU-NASA-RMC) |

# The Robot

The cad for the robot is located under \Robot CAD.

![View1](/Images/View1.png)

# Getting the Robot Setup

## Wire Connections
1. Check motor connections
2. Check camera connections

## Robot Computer
1. Make sure the robot is connected to the same Wi-Fi as the computer (internet not needed)
2. Run /Robot/RobotMain.py
3. Make note of the IP Address and Port it started up on

## Base Computer
1. Make sure the computer is connected to the same Wi-Fi as the robot (internet not needed)
2. Run /Base/BaseMain.py
   The GUI should start up.
3. Optional: Connect an x-box controller via usb to the computer and type command "joystick on" to start joystick control

## Startup
1. Type into the GUI "connect " + IP + Port
   Note: If IP is not specified it defaults to 192.168.0.100, and Port defaults to 23456
2. You are connected if the Info Text switches from "Not Connected" to "Connected"
3. Refer to the GUI section for more info

# The GUI

The GUI Consists of 5 elements:

1. Field view - Displays the position of the robot on the field
2. Camera views - Displays the images from each camera connected to the robot
3. Info Bar - Displays text information about the current robot status
4. Text Input Help - Displays command help
5. Text Input Box - Type commands into this

![GUIInfo](/Images/GUIInfo.png)

| Commands        | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| Connect IP Port | Connect to robot on given IP and Port                        |
| Other string    | Send string to robot with key="other"                        |
| Ping #          | Change communication frequency to # seconds                  |
| Joystick on/off | Turn on or off the sending of joystick data with key="joystick" |

# The Code

The code is split up into 2 different folders, Base and Robot. The base folder contains all the code that is required to interact with the robot. The robot folder is the same.

## Base

The base folder holds the files:

* BaseMain.py - Initialization
* commands.py - Parsing the commands from the GUI
* CommunicationBase.py - Communication between the robot and the GUI
* globals.py - Variables that are used in multiple files
* GUI.py - Runs the entire GUI
* Joystick.py - Joystick inputs

## Robot

The robot folder holds files:

* Cameras.py - Handles the cameras
* commands.py - Parsing the commands from Base, the StopEverything function is called continuously if the robot and base are disconnected
* CommunicationRobot.py - Communication between the robot and base
* globals.py - Variables that are used in multiple files
* motor.py - Controlling motors through the latte panda's onboard arduino
* RobotMain.py - Starts up everything, this is the only thread that is time sensitive, so all long tasks should be executed in the main wile loop in this thread.

