import os
import re
import time
import markdown2
from bs4 import BeautifulSoup


def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'      #define regular expression pattern to capture the song name
    match = re.search(pattern, command, re.IGNORECASE)   #use re.search to find the match in command
    return match.group(1) if match else None           #If a match is found return the extracted song name



def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()
    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)
    return result_string

def keyEvent(key_code):
    command = f'adb shell input keyword {key_code}'
    os.system(command)
    time.sleep(1)

def tapEvents(x,y):
    command = f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

def adbInput(message):
    command = f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

def replace_spaces_with_percent(input_string):
    return input_string.replace(' ','%s')

def markdown_to_text(md):
    html = markdown2.markdown(md)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()