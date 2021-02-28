from kivy.app import App
# from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
# from kivy.core.window import Window
# from kivy.uix.image import Image
from cv2 import *
# from kivy.graphics.texture import Texture
# from kivy.clock import Clock
# from kivy.uix.label import Label
import commands
import globals
import time

class GUI(Widget):
    def __init__(self, **kwargs):
        from kivy.uix.textinput import TextInput
        from kivy.core.window import Window
        from kivy.uix.image import Image
        from kivy.graphics.texture import Texture
        from kivy.clock import Clock
        from kivy.uix.label import Label
        super(GUI, self).__init__(**kwargs)

        # self.cam = VideoCapture(0)
        self.connected = [False,None]
        self.commandField = TextInput(pos = (200, 200), size = (100, 400), multiline = False)
        self.commandField.bind(on_text_validate = self.command_on_enter) ### first line
        # self.username.bind(text= self.on_text)  ### second line
        self.add_widget(self.commandField)
        Window.bind(on_resize = self.on_window_resize)

        self.AboveCommandText = Label(text = "Hello World",halign = "left",valign = "bottom")
        self.AboveCommandText.bind(size = self.AboveCommandText.setter('text_size')) #Actually aligns the text to left
        self.add_widget(self.AboveCommandText)

        self.InfoText = Label(text = "",halign = "left",valign = "top", markup=True)
        self.InfoText.bind(size = self.InfoText.setter('text_size'))
        self.add_widget(self.InfoText)

        self.FieldImage = Image()#,pos = (200,200),size = (200,200))
        self.CameraImage1 = Image()
        self.CameraImage2 = Image()
        self.CameraImage3 = Image()
        self.CameraImage4 = Image()
        self.add_widget(self.FieldImage)
        self.add_widget(self.CameraImage1)
        self.add_widget(self.CameraImage2)
        self.add_widget(self.CameraImage3)
        self.add_widget(self.CameraImage4)

        Clock.schedule_interval(self.Update_Screen, 1.0 / 33.0)

        self.on_window_resize(Window,Window.size[0],Window.size[1])

    def command_on_enter(self,value):
        command = value.text
        self.commandField.text = ""
        commands.parse(command)

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
        # self.InfoText.pos = (200,200)



    def img2Texture(self,img):
        from kivy.graphics.texture import Texture
        buf1 = cv2.flip(img, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        # if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        # self.image.texture = texture1
        return texture1


    def Update_Screen(self,x):
        import numpy as np
        # self.InfoText.text = str(globals.sharedData["DataRecieved"])
        if(globals.sharedData["NewDataRecieved"] == True):
            # frame =globals.sharedData["DataRecieved"]['CameraFrames'][0]
            # print(globals.sharedData["DataRecieved"]['CameraFrames'][0])
            Frames = []
            for frame in globals.sharedData["DataRecieved"]["CameraFrames"]:
                nparr = np.frombuffer(frame, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                Frames.append(frame)

            if(len(Frames) >= 1):   # This should be a switch statement, but python switch statements are funky
                self.CameraImage1.texture = self.img2Texture(Frames[0])
            if(len(Frames) >= 2):
                self.CameraImage2.texture = self.img2Texture(Frames[1])
            if (len(Frames) >= 3):
                self.CameraImage3.texture = self.img2Texture(Frames[2])
            if (len(Frames) >= 4):
                self.CameraImage4.texture = self.img2Texture(Frames[3])

            globals.sharedData["NewDataRecieved"] = False
            self.connected = globals.sharedData["ConnectedAddress"]
        ping = time.time()-globals.sharedData["LastConnectTime"]
        text = ""
        if (ping < 3):
            text = text + "[color=#9af075]Connected: \n   " + str(self.connected[0]) + "\n   " + str(self.connected[1]) + "[/color]\n"
            text = text + "Ping: " + ("%.2f" % (ping))
        else:
            text = text + "[color=#fa9134]Not Connected[/color]\n"

        self.InfoText.text = text

    # def GUIUpdateText(self,command,update):
    #     if(command == "connected"):
    #         self.connected = update
    #     text = ""
    #     if(self.connected[0] == True):
    #         text = text + "[color=9af075]Connected: " + str(self.connected[1]) + "[/color]\n"
    #     else:
    #         text = text + "[color=fa9134]Not Connected[/color]\n"
    #
    #     text = text + "Ping: " + ("%.1f" % time.time()-globals.sharedData["LastConnectTime"])
    #
    #     self.InfoText.text = text
    #
    # def on_text(instance, value, secondvalue):
    #     print(secondvalue)


class GUIApp(App):
    def build(self):
        return GUI()


# if __name__ == "__main__":
#     GUIApp().run()