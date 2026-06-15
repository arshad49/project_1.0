# main.py
from flask import Flask, render_template_string
from flask_socketio import SocketIO
import threading
import datetime
import speech_recognition as sr

from web import open_website
from edge import speak  # Only used for local TTS fallback, optional
from time_date import current_time, current_date, current_day, current_month, current_year
from commands import open_app, close_app
from mood import get_mood
from name_saved import name_asked
from memory import save_name, load_name
from reminder import start_reminder_thread, handle_reminder
import requests

# -----------------------------
# Flask + SocketIO setup
# -----------------------------
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# -----------------------------
# Frontend HTML + CSS + JS
# -----------------------------
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JarvisNova</title>
<style>
body { font-family:sans-serif; background:#111; color:#0ff; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; }
.container { width:90%; max-width:600px; border:2px solid #0ff; padding:20px; border-radius:10px; background:rgba(0,0,0,0.7);}
#messages { height:400px; overflow-y:auto; border-top:1px solid #0ff; padding-top:10px; }
p { margin:5px 0; }
.assistant { color:#0ff; }
.user { color:#faa500; }
</style>
</head>
<body>
<div class="container">
<h1>JarvisNova</h1>
<div id="messages">
<p class="assistant">👋 JarvisNova is online...</p>
</div>
</div>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
const socket = io();
const messages = document.getElementById('messages');

socket.on('assistant_output', data => {
  const p = document.createElement('p');
  p.textContent = data.message;
  p.className = 'assistant';
  messages.appendChild(p);
  messages.scrollTop = messages.scrollHeight;

  // Browser speaks only if speak=true
  if(data.speak){
    const utterance = new SpeechSynthesisUtterance(data.message);
    speechSynthesis.speak(utterance);
  }
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

# -----------------------------
# Global flags
# -----------------------------
running = True
greeted_once = False

# -----------------------------
# Utility function to send messages to frontend
# -----------------------------
def send_to_frontend(message: str, speak=False):
    """Send message to frontend and terminal."""
    print(">>", message)  # terminal log
    socketio.emit('assistant_output', {'message': message, 'speak': speak})

# -----------------------------
# Assistant functions (original)
# -----------------------------
def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        send_to_frontend("🎧 Adjusting for ambient noise...", speak=False)
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        send_to_frontend("🎤 Listening...", speak=False)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        send_to_frontend(f"🗣 You said: {text}", speak=False)
        return text
    except sr.UnknownValueError:
        send_to_frontend("❌ Could not understand audio.", speak=False)
    except sr.RequestError as e:
        send_to_frontend(f"⚠️ Could not request results; {e}", speak=False)
    return None

def greet_user():
    name = load_name()
    hour = datetime.datetime.now().hour

    if not name:
        name_asked()
        name = load_name()

    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    send_to_frontend(f"{greeting} {name}, how are you today?", speak=True)
    user_reply = listen()
    mood = get_mood(user_reply if user_reply else "")

    if mood == "happy":
        extra_message = "I hope you're having a great day!"
    elif mood == "sad":
        extra_message = "I hope things get better soon!"
    else:
        extra_message = "I hope you're doing well!"

    send_to_frontend(f"{extra_message}, How can I help you today?", speak=True)

def command_listener(direct_command=None):
    global running
    while running:
        command = direct_command if direct_command else listen()
        direct_command = None

        if command:
            command = command.lower()
            exit_cmd = ["exit", "quit", "stop", "close", "goodbye", "bye", "terminate", "end"]

            if any(phrase in command for phrase in exit_cmd):
                send_to_frontend("Goodbye!", speak=True)
                running = False
                break
            elif "open" in command:
                item = command.replace('open', '').strip()
                send_to_frontend(f"Opening {item}", speak=True)
                open_website(item)
            elif "close" in command or "quit" in command:
                item = command.replace('close', '').replace('quit', '').strip()
                send_to_frontend(f"Closing {item}", speak=True)
                response = close_app(item)
                send_to_frontend(response, speak=True)
            elif any(phrase in command for phrase in ["time", "clock", "date", "day", "month", "year"]):
                response = ""
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
                send_to_frontend(response.strip(), speak=True)
            
            elif "greet" in command:
                try:
                    response = requests.get('http://127.0.0.1:5000/greet')
                    if response.status_code == 200:
                        send_to_frontend(response.json().get('message'), speak=True)
                except requests.exceptions.RequestException as e:
                    send_to_frontend(f"Error connecting to Flask server: {e}", speak=False)
            else:
                send_to_frontend(f"You said: {command}", speak=True)

            # Handle reminders
            if handle_reminder(command):
                continue

            break

def wake_up_listener():
    global running, greeted_once
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        send_to_frontend("🎧 Adjusting for ambient noise for wake-up listener...", speak=False)
        recognizer.adjust_for_ambient_noise(source, duration=0.3)

    while running:
        send_to_frontend("Waiting for wake word...", speak=False)
        command = listen()
        if not command:
            continue

        lower_cmd = command.lower()
        if "nova" in lower_cmd:
            after_wake = lower_cmd.split("nova", 1)[-1].strip()

            if not greeted_once:
                greet_user()
                greeted_once = True
            command_listener(direct_command=after_wake)

# -----------------------------
# Main
# -----------------------------
def main():
    global greeted_once
    greeted_once = False
    start_reminder_thread()
    # Start assistant loop in background thread
    threading.Thread(target=wake_up_listener, daemon=True).start()
    # Start Flask + SocketIO server
    socketio.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    main()
