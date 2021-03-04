from cv2 import *
import commands
import globals
import time

# Set up GUI, to run initilize it and use InitilizeGUI() and GUIApp().run()
def InitilizeGUI():
    # Imports inside the initilize so other processes don't load unnecessary data
    from kivy.app import App
    from kivy.uix.widget import Widget

    # GUI contains all the information to build the GUI and how it reacts to inputs
    global GUI
    class GUI(Widget):
        def __init__(self, **kwargs):
            from kivy.uix.textinput import TextInput
            from kivy.core.window import Window
            from kivy.uix.image import Image
            from kivy.clock import Clock
            from kivy.uix.label import Label
            super(GUI, self).__init__(**kwargs)

            self.connected = [False,None] # Initilize ip-address and port to display

            # Place the command box that commands are typed into
            self.commandField = TextInput(pos = (200, 200), size = (100, 400), multiline = False)
            self.commandField.bind(on_text_validate = self.command_on_enter)
            self.add_widget(self.commandField)
            Window.bind(on_resize = self.on_window_resize)

            # TODO show expected command and command inputs/flags
            # Text above the command box
            self.AboveCommandText = Label(text = "Hello World",halign = "left",valign = "bottom")
            self.AboveCommandText.bind(size = self.AboveCommandText.setter('text_size')) #Actually aligns the text to left
            self.add_widget(self.AboveCommandText)

            # Text on the right side that displays connection info
            self.InfoText = Label(text = "",halign = "left",valign = "top", markup=True)
            self.InfoText.bind(size = self.InfoText.setter('text_size'))
            self.add_widget(self.InfoText)

            # Images for the field and from the cameras
            self.FieldImage = Image()
            self.CameraImage1 = Image()
            self.CameraImage2 = Image()
            self.CameraImage3 = Image()
            self.CameraImage4 = Image()
            self.add_widget(self.FieldImage)
            self.add_widget(self.CameraImage1)
            self.add_widget(self.CameraImage2)
            self.add_widget(self.CameraImage3)
            self.add_widget(self.CameraImage4)

            # Set GUI to check for updates periodically
            Clock.schedule_interval(self.Update_Screen, 1.0 / 33.0)

            # Call the function that sets the widgets to the correct size
            self.on_window_resize(Window,Window.size[0],Window.size[1])

        # This is called when a command is entered and the enter button is pressed
        # Executes the command parser, which evaluates what to do with the command
        def command_on_enter(self,value):
            command = value.text
            self.commandField.text = ""
            commands.parse(command)

        # This is called when the window is resized
        # Sets the various widgets to the correct size to fit into the window
        def on_window_resize(self,window,width,height):
            seperation = width*(1/80)
            fontSize = height / 20 - 15
            InfoTextWidth = width/5

            self.commandField.size = (width-2*seperation, height / 20)
            self.commandField.pos = (seperation, seperation)
            self.commandField.font_size = fontSize

            self.AboveCommandText.size = self.commandField.size
            self.AboveCommandText.pos = (seperation, self.commandField.pos[1]+self.commandField.size[1]+.5*seperation)
            self.AboveCommandText.font_size = fontSize
            self.AboveCommandText.bind(size=self.AboveCommandText.setter('text_size'))

            self.FieldImage.pos = (seperation, self.AboveCommandText.pos[1]+self.AboveCommandText.font_size+seperation)
            FieldHeight = height-(self.FieldImage.pos[1]+seperation)
            self.FieldImage.size = ((2/6)*FieldHeight,FieldHeight)

            CameraWidth = (width-5*seperation-self.FieldImage.size[0]-InfoTextWidth)/2
            self.CameraImage1.size = (CameraWidth,CameraWidth*1080/1920)
            self.CameraImage1.pos = (self.FieldImage.pos[0]+self.FieldImage.size[0]+seperation,height-seperation-self.CameraImage1.size[1])

            self.CameraImage2.size = (CameraWidth, CameraWidth * 1080 / 1920)
            self.CameraImage2.pos = (self.CameraImage1.pos[0] + self.CameraImage1.size[0] + seperation, height - seperation - self.CameraImage1.size[1])

            self.CameraImage3.size = (CameraWidth, CameraWidth * 1080 / 1920)
            self.CameraImage3.pos = (self.CameraImage1.pos[0], self.CameraImage1.pos[1]-self.CameraImage1.size[1]-seperation)

            self.CameraImage4.size = (CameraWidth, CameraWidth * 1080 / 1920)
            self.CameraImage4.pos = (self.CameraImage2.pos[0],self.CameraImage3.pos[1])

            self.InfoText.font_size = fontSize
            self.InfoText.bind(size=self.InfoText.setter('text_size'))
            self.InfoText.pos = (self.CameraImage4.pos[0]+self.CameraImage4.size[0]+seperation, self.AboveCommandText.pos[1]+self.AboveCommandText.size[1]+seperation)
            self.InfoText.size = (InfoTextWidth - 2*seperation, height - self.InfoText.pos[1]-seperation)

        # Converts a cv2 image to texture that can be applied to an Image widget
        def img2Texture(self,img):
            from kivy.graphics.texture import Texture
            buf1 = cv2.flip(img, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            return texture1

        # This is called 30x per second and handels the updating of info on the screen
        def Update_Screen(self,x):
            import numpy as np
            globals.ThreadLocker.acquire()
            NewData = globals.sharedData.copy()
            globals.ThreadLocker.release()

            if(NewData["NewDataRecieved"] == True):
                globals.ThreadLocker.acquire()
                globals.sharedData["NewDataRecieved"] = False
                globals.ThreadLocker.release()

                Frames = [] # Get camera frames from the data, and turn them into image objects
                for frame in NewData["DataRecieved"]["CameraFrames"]:
                    nparr = np.frombuffer(frame, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    Frames.append(frame)

                # Update the GUI textures with the camera frames
                if(len(Frames) >= 1):   # This should be a switch statement, but python switch statements are funky
                    self.CameraImage1.texture = self.img2Texture(Frames[0])
                if(len(Frames) >= 2):
                    self.CameraImage2.texture = self.img2Texture(Frames[1])
                if (len(Frames) >= 3):
                    self.CameraImage3.texture = self.img2Texture(Frames[2])
                if (len(Frames) >= 4):
                    self.CameraImage4.texture = self.img2Texture(Frames[3])

            # Build the info text block
                self.connected = NewData["ConnectedAddress"]
            ping = time.time()-NewData["LastConnectTime"]
            text = ""
            # Connected
            if (ping < 3*(NewData["LocalPing"]+.1) and NewData["ConnectionStatus"] == 0):
                text = text + "[color=#9af075]Connected: \n   " + str(self.connected[0]) + "\n   " + str(self.connected[1]) + "[/color]\n"
                text = text + "Ping: " + ("%.2f" % (ping))
            # Attempting reconnection
            elif (NewData["ConnectionStatus"] == 1):
                text = text + "[color=#e6ed21]Reconnecting... \n   " + str(self.connected[0]) + "\n   " + str(
                    self.connected[1]) + "[/color]\n"
                text = text + "Ping: " + ("%.2f" % (ping))
            # Not connected or lost
            else:
                text = text + "[color=#fa9134]Not Connected[/color]\n"

            self.InfoText.text = text

    global GUIApp
    class GUIApp(App):
        def build(self):
            return GUI()