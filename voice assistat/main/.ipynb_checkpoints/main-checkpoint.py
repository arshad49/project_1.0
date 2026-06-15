import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import speech_recognition as sr
# import datetime
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Speed of speech

def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()
from speech.speaker import speak
from emotion.mood import get_mood
# from memory.memory import save_memory, load_memory
from commands.time_date import  current_time, current_date, current_month, current_day, current_year
from commands.commands import open_app, close_app

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError as e:
        speak(f"Could not request results; {e}")

def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    speak(f"{greeting}, How can I help you today?")

def main():
    while True:
        command = listen()
        if command:
            command = command.lower()
            exit_cmd = ["exit", "quit", "stop", "close", "goodbye", "bye", "see you later", "terminate", "end"]
            if any(phrase in command for phrase in exit_cmd):
                speak("Goodbye!")
                break
            elif "open" in command:
                item = command.replace('open', '').strip()
                speak(f"Opening {item}")
                response = open_app(command)
                speak(response)
            elif "close" in command or "quit" in command:
                item = command.replace('close', '').replace('quit', '').strip()
                speak(f"Closing {item}")
                response = close_app(command)
                speak(response)
            elif any(phrase in command for phrase in ["time", "clock","date", "day", "month", "year"]):
                response=""
                if "date" in command:
                    response += f"Today's date is {current_date()}.\n"
                if "time" in command:
                    response += f"The current time is {current_time()}.\n"
                if "day" in command:    
                    response += f"Today is {current_day()}.\n"
                if "month" in command:
                    response += f"The current month is {current_month()}.\n"
                if "year" in command:       
                    response += f"The current year is {current_year()}.\n"
                speak(response.strip())
            else:
                speak(f"You said: {command}")

if __name__ == "__main__":
    greet_user()
    main()
