import speech_recognition as sr
import edge_tts
import pyttsx3
recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine=pyttsx3.init
def speak(text):
    engine.say(text)
    engine.runAndWait()
    

def wake_up():
    with microphone as source:
        audio=recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command= recognizer.recognize_google(audio)
        print(f"You said: {command}")

        if "hey nova" in command.lower():
            print("Wake word detected!")
            speak("Hello, how can I assist you?")
            return True
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    return False

def listen_loop():
    while True:
        if wake_up():
            break