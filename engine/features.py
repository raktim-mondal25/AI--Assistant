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
import google.generativeai as genai  # ✅ Gemini import


# ======================================================
# ✅ GEMINI CONFIGURATION
# ======================================================
GEMINI_API_KEY = "AIzaSyDL3NWMOHQOdo4F8up9sK0AY522vVXdNHw" 

try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ Gemini initialized successfully")
except Exception as e:
    print(f"❌ Gemini initialization failed: {e}")
    model = None


def chat_with_gemini(prompt):
    """Send user input to Gemini and return its response."""
    try:
        if not model:
            return "Model not initialized."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# ======================================================
# ✅ DATABASE SETUP
# ======================================================
con = sqlite3.connect("friday.db")
cursor = con.cursor()

# ======================================================
# ✅ ASSISTANT CORE FUNCTIONS
# ======================================================
@eel.expose
def playAssistantSound():
    music_dir = "www\\assests\\audio\\notification-sound-effect-372475.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip()
    app_name = query

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
                    os.startfile(results[0][0])
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
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


# ======================================================
# ✅ HOTWORD ACTIVATION
# ======================================================
def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
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


# ======================================================
# ✅ CONTACT & WHATSAPP FUNCTIONS
# ======================================================
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts_table WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
                       ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 19
        jarvis_message = "message sent successfully to " + name
    elif flag == 'call':
        target_tab = 14
        message = ''
        jarvis_message = "calling " + name
    elif flag == 'video call':
        target_tab = 13
        message = ''
        jarvis_message = "starting video call with " + name

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)

    autogui.hotkey('ctrl', 'f')
    for i in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.hotkey('enter')
    speak(jarvis_message)


# ======================================================
# ✅ ANDROID AUTOMATION
# ======================================================
def makecall(name, mobileno):
    mobileno = mobileno.replace(" ", "")
    speak("Calling " + name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:' + mobileno
    os.system(command)


def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent(message)
    mobileNo = replace_spaces_with_percent(mobileNo)
    speak("Sending message")
    tapEvents(341.8, 2234.1)
    tapEvents(793.5, 2212.6)
    adbInput(mobileNo)
    tapEvents(349.5, 742.5)
    tapEvents(243.5, 2228.3)
    adbInput(message)
    tapEvents(958.0, 1401.1)
    speak("Message sent successfully to " + name)


# ======================================================
# ✅ GEMINI CHAT INTEGRATION FUNCTION (Voice + Chat)
# ======================================================
import threading

@eel.expose
def geminiAssistant(prompt):
    try:
        print(f"\n🎯 Gemini Prompt: {prompt}\n")
        response = chat_with_gemini(prompt)

        print("📩 Raw Gemini Response object:", response)   # 👈 add this line

        if not response or response.strip() == "":
            response = "Sorry, I couldn't generate a response right now."

        clean_response = re.sub(r'\*{1,2}', '', response)
        clean_response = clean_response.replace("\n", " ").strip()

        print(f"🧠 Gemini Response (cleaned): {clean_response}\n")

        threading.Thread(target=lambda: speak(clean_response)).start()
        return clean_response

    except Exception as e:
        error_msg = f"Error while using Gemini: {e}"
        print(error_msg)
        threading.Thread(target=lambda: speak("Sorry, I faced an error while generating the response.")).start()
        return error_msg
