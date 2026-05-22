import pyttsx3
import speech_recognition as sr
import eel
import time
import threading
import queue
def ui(func, *args):
    eel.spawn(func, *args)



speech_requests = queue.Queue()
speech_ready = threading.Event()
speech_engine_error = None


def _speech_worker():
    global speech_engine_error

    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 164)
    except Exception as error:
        speech_engine_error = error
        speech_ready.set()
        return

    speech_ready.set()
    while True:
        text, completed = speech_requests.get()
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as error:
            print("Speak error:", error)
        finally:
            completed.set()
            speech_requests.task_done()


threading.Thread(target=_speech_worker, daemon=True).start()

# --- GLOBAL SPEECH OBJECTS ---
recognizer = sr.Recognizer()
mic = sr.Microphone()


def speak(text):
    try:
        print("Speaking:", text)
        eel.DisplayMessage(text)
        ui(eel.receiverText,text)
    except Exception as e:
        print("Speech display error:", e)

    normalized_text = text.casefold()
    if (normalized_text.startswith("playing ") and normalized_text.endswith(" on youtube")) or normalized_text.startswith("message sent successfully to "):
        return

    if not speech_ready.wait(timeout=10):
        print("Speech engine did not initialize")
        return
    if speech_engine_error is not None:
        print("Speech engine error:", speech_engine_error)
        return

    completed = threading.Event()
    speech_requests.put((text, completed))
    completed.wait()
    time.sleep(0.3)



def takecommand():
    global recognizer, mic

    try:
        with mic as source:
            print("Listening....")
            eel.DisplayMessage("Listening....")

            recognizer.pause_threshold = 1
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        print("Recognizing....")
        eel.DisplayMessage("Recognizing....")

        query = recognizer.recognize_google(audio, language='en-in')
        print("User said:", query)
        eel.DisplayMessage(query)

        return query.lower()

    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print("Mic error:", e)
        return ""



@eel.expose
def allCommands(message=1):
    _allCommandsWorker(message)
    return "done"


def _allCommandsWorker(message=1):
    
    if message==1:
        query = takecommand()
        print(query)
        ui(eel.senderText, query)
    else:
        query = message
        ui(eel.senderText,query)
    
    if not query.strip():
        speak("Sorry, I didn't catch that. Please try again.")
        return



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
            from engine.features import geminai
            geminai(query)
    except Exception as e:
        print("Command error:", e)