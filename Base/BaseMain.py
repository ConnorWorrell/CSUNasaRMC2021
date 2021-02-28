import GUI
import CommunicationBase
import globals

if __name__ == '__main__':
    globals.initilizeGlobals()
    GUI.InitilizeGUI()
    # pass
    # CommunicationBase.ListenForData(None)
    # print(globals.dataToSend)
    # pass
    # CommunicationBase.StartProcess("0")
    GUIApp = GUI.GUIApp()
    GUIApp.run()