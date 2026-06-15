import threading
import time
import datetime
import json
import speech_recognition as sr
from edge import speak  # Replace with your own speak() if needed

reminders = []

def save_reminders():
    with open('reminders.json', 'w') as f:
        json.dump(reminders, f)

def load_reminders():
    global reminders
    try:
        with open('reminders.json', 'r') as f:
            reminders = json.load(f)
    except FileNotFoundError:
        reminders = []

def set_reminder(task, reminder_time):
    reminder = {
        'task': task,
        'time': reminder_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    reminders.append(reminder)
    save_reminders()
    print(f"Reminder set for '{task}' at {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}.")

def notify_user(task):
    print(f"Reminder: {task}")
    speak(f"Reminder: {task}")

def check_reminders():
    while True:
        try:
            now = datetime.datetime.now()
            for reminder in reminders[:]:
                reminder_time = datetime.datetime.strptime(reminder['time'], '%Y-%m-%d %H:%M:%S')
                delta = (now - reminder_time).total_seconds()

                if 0 <= delta < 60:
                    notify_user(reminder['task'])
                    reminders.remove(reminder)
                    save_reminders()
            time.sleep(30)
        except Exception as e:
            print(f"Error in reminder check: {e}")
            time.sleep(30)

def start_reminder_thread():
    load_reminders()
    threading.Thread(target=check_reminders, daemon=True).start()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return None

def parse_time_input(text):
    now = datetime.datetime.now()
    text = text.lower().strip()

    if "in" in text:
        try:
            after_in = text.split("in", 1)[1].strip()
            words = after_in.split()
            number = None
            for w in words:
                if w.isdigit():
                    number = int(w)
                    break
            if number is None:
                return None
            if "minute" in after_in:
                return now + datetime.timedelta(minutes=number)
            elif "hour" in after_in:
                return now + datetime.timedelta(hours=number)
            else:
                return None
        except:
            return None

    if "at" in text:
        try:
            time_part = text.split("at", 1)[1].strip()
            try:
                dt_time = datetime.datetime.strptime(time_part, "%I %p")
            except ValueError:
                dt_time = datetime.datetime.strptime(time_part, "%H:%M")
            return now.replace(hour=dt_time.hour, minute=dt_time.minute, second=0, microsecond=0)
        except:
            return None

    return None

def read_reminders():
    load_reminders()
    if not reminders:
        speak("You have no reminders set.")
        return
    speak("Here are your upcoming reminders:")
    for reminder in reminders:
        task = reminder['task']
        time_str = reminder['time']
        speak(f"to {task} at {time_str}")

def delete_reminder(identifier):
    load_reminders()
    found = False
    global reminders
    ident = identifier.lower()
    new_reminders = []
    for r in reminders:
        task = r['task'].lower()
        time_str = r['time'].lower()
        if ident in task or ident in time_str:
            found = True
        else:
            new_reminders.append(r)
    if found:
        reminders = new_reminders
        save_reminders()
    return found

def handle_reminder(command):
    command = command.lower()

    delete_keywords = [
        "delete reminder", "remove reminder", "cancel reminder", "clear reminder"
    ]
    if any(k in command for k in delete_keywords):
        for dk in delete_keywords:
            if dk in command:
                identifier = command.split(dk, 1)[1].strip()
                if identifier == "":
                    speak("Please tell me what reminder to delete.")
                    return True
                if delete_reminder(identifier):
                    speak(f"Deleted reminder matching '{identifier}'.")
                else:
                    speak(f"No reminder found matching '{identifier}'.")
                return True

    show_keywords = [
        "show reminders", "show me the reminders", "list reminders", "what are my reminders",
        "read reminders", "reminders list", "upcoming reminders"
    ]
    if any(k in command for k in show_keywords):
        read_reminders()
        return True

    keywords = [
        "remind me to", "set reminder", "schedule a reminder for",
        "please remind me to", "i need a reminder to", "alert me to",
        "don't let me forget to", "make a note to", "ping me to"
    ]
    for keyword in keywords:
        if keyword in command:
            task_with_time = command.split(keyword, 1)[1].strip()
            if " at " in task_with_time:
                parts = task_with_time.rsplit(" at ", 1)
                task = parts[0].strip()
                time_expr = "at " + parts[1].strip()
            elif " in " in task_with_time:
                parts = task_with_time.rsplit(" in ", 1)
                task = parts[0].strip()
                time_expr = "in " + parts[1].strip()
            else:
                speak("Sorry, I couldn't find a time in your reminder.")
                return True
            remind_time = parse_time_input(time_expr)
            if remind_time:
                set_reminder(task, remind_time)
                speak(f"Reminder set for {task}")
            else:
                speak("Sorry, I didn't understand the time.")
            return True

    return False
