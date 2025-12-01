import re
from shlex import quote
import struct
import time
import playsound as playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from backend import env
from backend.command import speak
from backend.config import ASSISTANT_NAME
import os
import subprocess
import webbrowser
import pywhatkit as kit
import sqlite3


from backend.helper import extract_search_term, remove_words
conn=sqlite3.connect("javis.db")
cursor=conn.cursor()
@eel.expose
def playAssistantSound():
    music_dir="frontend\\assets\\audio\\start_sound.mp3"
    playsound.playsound(music_dir)

@eel.expose
def openCommand(query):
    query=query.replace(ASSISTANT_NAME,"")
    query=query.replace("open","")
    query=query.lower()
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")
@eel.expose
def youtube(query):
    search_term=extract_search_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)




import speech_recognition as sr

HOTWORDS = ["jarvis", "alexa", "spark", "assistant"]

def hotword():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening for hotword... (Jarvis / Alexa)")

        while True:
            try:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

                try:
                    text = r.recognize_google(audio).lower()
                    print("Heard:", text)

                    # Check if any hotword exists in recognized speech
                    for word in HOTWORDS:
                        if word in text:
                            print("🔥 Hotword Detected:", word)

                            # Trigger your shortcut WIN + J
                            pyautogui.keyDown("win")
                            pyautogui.press("j")
                            pyautogui.keyUp("win")

                            print("⚡ Shortcut Triggered (WIN + J)")
                            time.sleep(2)

                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    print("⚠️ Internet Issue with Google Recognition")

            except KeyboardInterrupt:
                print("Stopped hotword detection.")
                break




def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

@eel.expose  


def whatsApp(phone, message, flag, name):
    # Path to WhatsApp Desktop shortcut
    whatsapp_path = r"D:\OneDrive\Desktop\WhatsApp.lnk"

    # Open WhatsApp Desktop
    subprocess.Popen(['start', '', whatsapp_path], shell=True)
    time.sleep(6)  # wait for WhatsApp to launch

    # Search for the contact
    pyautogui.hotkey("ctrl", "f")  
    time.sleep(1)
    pyautogui.typewrite(name)  # type contact name
    time.sleep(1)
    pyautogui.press("enter")

    if flag == "message":
        pyautogui.typewrite(message)
        pyautogui.press("enter")
        print(f"✅ Message sent to {name}")

    elif flag == "call":
        call_btn = pyautogui.locateOnScreen(r"D:\OneDrive\Desktop\assets\call_button.png", confidence=0.8)
        if call_btn:
            pyautogui.click(call_btn)
            print(f"📞 Calling {name}...")
        else:
            print("❌ Call button not found on screen")

    elif flag == "video":
        video_btn = pyautogui.locateOnScreen("video_button.png", confidence=0.8)
        if video_btn:
            pyautogui.click(video_btn)
            print(f"🎥 Starting video call with {name}...")
        else:
            print("❌ Video call button not found on screen")



import google.generativeai as genai
from backend.env import GEMINI_API_KEY

def chat_with_bot(query):
    # Set your Gemini API key
    genai.configure(api_key=GEMINI_API_KEY)  # Replace with your actual API key

    # Personal details
    USER_NAME = "rajashekhar"
    BOT_NAME = "Jarvis"

    # List of friends with their relationship
    friends = {
        "sumit": "rajashekhar's friend",
        "vikas":"rajashekhar's friend and roomate",
        "sai teja":"rajashekhar's friend",
        "ravikiran":"rajashekhar's friend",
    }

    # Build dynamic friend context
    friend_lines = [
        f"If someone asks 'Who is {name}?' you should say '{name} is {relation}.'"
        for name, relation in friends.items()
    ]
    friends_prompt = "\n".join(friend_lines)

    # Complete system prompt
    system_prompt = (
        f"You are an intelligent AI assistant named {BOT_NAME}. "
        f"Your creator and main user is {USER_NAME}. "
        f"If someone asks 'Who is {BOT_NAME}?' you should say you are a virtual assistant created by {USER_NAME}. "
        f"If someone asks 'Who is {USER_NAME}?' you should say that is your creator and primary user. "
        f"{friends_prompt} "
        f"Always answer respectfully and concisely."
    )

    # Combine prompt with user query
    full_prompt = f"{system_prompt}\nUser: {query}\n{BOT_NAME}:"

    # Generate response
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(full_prompt)
    return response.text
    



from datetime import datetime

def timeNow():
    now = datetime.now()
    hour = now.strftime("%I")      # 12-hour format
    minute = now.strftime("%M")
    period = now.strftime("%p")    # AM or PM

    time_text = f"the time is {hour} o clock {minute} minutes {period}"
    return time_text