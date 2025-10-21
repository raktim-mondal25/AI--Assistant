import os
import eel 

from engine.features import *    #accessing the features from features.py
from engine.command import *    #accessing the command from command.py           
from engine.auth import recognize
def start():
    eel.init("www")

    flag = recognize.AuthenticateFace()
    playAssistantSound()
    speak("Welcome back. Fell free to tell me what I could do for You")
    # for opening in app mode
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')   
    # assigning the frontend file to start this
    eel.start('index.html', mode=None, host='localhost', block=True)