import pyttsx3
import speech_recognition as sr
import eel
import time

# Speak function, including setting the voice[male/female], speed and volume.ss
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 164)      
    eel.DisplayMessage(text)
    # print(voices)             # to print the voices available
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening....")
        eel.DisplayMessage("Listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        print("Recognizing....")
        eel.DisplayMessage("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        # speak(query)            #calling the speak function so that it can understand what is saids
    except Exception as e:
        return ""
    
    return query.lower()


@eel.expose
def allCommands(message=1):
    
    if message==1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)


    try:
        # query = takecommand()
        # print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makecall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no!=0):
                speak("Which mode you want to use whatsapp or mobile")
                preference = takecommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query:
                        speak("What message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makecall(name, contact_no)
                    else:
                        speak("Please try again")

                elif "whatsapp" in preference:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("What message to send")
                        query = takecommand()
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                    whatsApp(contact_no, query, message, name)

        else:
            print("Not run")
    except:
        print("error")

    eel.Showhood()