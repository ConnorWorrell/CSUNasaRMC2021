import GUI
import globals

if __name__ == '__main__':
    # Initilize Global Variables
    globals.initilizeGlobals()

    # Start GUI
    GUI.InitilizeGUI()
    GUIApp = GUI.GUIApp()
    GUIApp.run()