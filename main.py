import os
import eel
from backend.auth import recoganize
from backend.feature import *
from backend.command import *

def start():
    eel.init('frontend')
    playAssistantSound()
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Welcome to Jarvis")
        speak("ready for face authentication")
       
        flag=recoganize.AuthenticateFace()
        if flag==1:
            speak("Face recognized successfully")
            eel.hideFaceAuth()
            eel.hideFaceAuthSuccess()
            speak("welcome to your Assistant")
            eel.hideStart()
            eel.showChat()
            playAssistantSound()
        else:
            speak("Face not recognized. Please try again.") 


    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host="localhost",block=True)
