from memory import save_name
from edge import speak
import speech_recognition as sr

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
def name_asked():
    speak("Hello, I don't know your name. Please tell me your name.")
    name = listen()
    if name:
        save_name(name)
        print(f"Name saved: {name}")
        speak(f"Nice to meet you, {name}!")
    else:
        speak("I didn't catch your name, but nice to meet you anyway!")
    
