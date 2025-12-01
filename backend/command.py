import pyttsx3
import eel


@eel.expose
def speak(text):
    text = str(text)

    # Show immediately
    
    eel.receiverText(text)

    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    
    # Speak after showing
    # print(text)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
   
 # Display the assistant's response in the chat interface

@eel.expose
def takeCommand():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=8, phrase_time_limit=10)
  
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        speak(query)
    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    query= query.lower()
    return query

@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takeCommand()  # If no message is passed, listen for voice input
        if not query:
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)  # Display the recognized text in the chat interface
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)  # Display the recognized text in the chat interface
    
    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            # in your main command handler
            elif "send message" in query or "video call" in query or "call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        message = takeCommand()  # capture actual message text
                    elif "video call" in query:
                        flag = 'video'          # use 'video' to match whatsApp() check
                        message = ''
                    else:  # "call" in query
                        flag = 'call'
                        message = ''

                    whatsApp(Phone, message, flag, name)


            elif "on youtube" in query:
                from backend.feature import youtube
                youtube(query)
            elif "time now" in query:
                from backend.feature import timeNow
                current_time = timeNow()
                speak(current_time)
            else:
                from backend.feature import chat_with_bot
                response=chat_with_bot(query)
                speak(response)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
    
      # Call this from frontend after animation completes
    eel.ShowHood()