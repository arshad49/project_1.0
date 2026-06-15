import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Speed of speech

def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()