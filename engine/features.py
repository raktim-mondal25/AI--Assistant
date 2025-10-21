import os
import re
from shlex import quote
import subprocess
import time
import traceback
import webbrowser
from engine.command import allCommands, speak
from engine.helper import extract_yt_term, remove_words
from playsound import playsound
import eel
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import sqlite3
import pvporcupine
import pyaudio
import struct
import pyautogui as autogui



con = sqlite3.connect("friday.db")
cursor = con.cursor()

# playing assistant sound function

@eel.expose
def playAssistantSound():
    music_dir ="www\\assests\\audio\\notification-sound-effect-372475.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    # if query!="":
    #     speak("Openning "+query)
    #     os.system('start '+query)
    # else:
    #     speak(f"Sorry, I could not find {query}")
    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            else:
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    os.startfile(results[0][0]) # it removes the brackets as it is present within a tuple
                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + app_name)
                    except Exception:
                        speak("Not found")
        except Exception as e:
            speak("Something went wrong")
            print("Error:", e)


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)



# to active it by just calling its name
def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        # Use built-in keyword only, e.g. "alexa", "computer", "porcupine"
        porcupine = pvporcupine.create(keywords=["computer"])

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,
                                 channels=1,
                                 format=pyaudio.paInt16,
                                 input=True,
                                 frames_per_buffer=porcupine.frame_length)

        print("Listening for hotword...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)

            if result >= 0:
                print("Hotword detected!")
                autogui.hotkey("win", "j")
                time.sleep(1)

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts_table WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    



# Whatsapp function(Very Important)
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 19
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 14
        message = ''
        jarvis_message = "calling to "+name

    elif flag == 'video call':
        target_tab = 13
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    autogui.hotkey('ctrl', 'f')   #it will find the name in the whatsapp automatically

    for i in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.hotkey('enter')
    speak(jarvis_message)



# android automation
def makecall(name, mobileno):
    mobileno = mobileno.replace(" ","")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileno
    os.system(command)


def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent(message)
    mobileNo = replace_spaces_with_percent(mobileNo)
    speak("Sending message")
    # goback(1)
    # time.sleep(1)
    # keyEvent(3)
    # open sms app
    tapEvents(341.8,2234.1)
    # start chat
    tapEvents(793.5,2212.6)
    # search mobile number
    adbInput(mobileNo)
    # tap on name
    tapEvents(352.8,585.5)
    # tap on input
    tapEvents(243.5,2228.3)
    #type message
    adbInput(message)
    # send
    tapEvents(958.0,1401.1)
    speak("Message sent successfully to "+name)