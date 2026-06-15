import os

def open_app(command):
    command = command.lower()
    if "notepad" in command:
        os.system("open -a TextEdit")
    elif "calculator" in command:
        os.system("open -a Calculator")
    elif "safari" in command:
        os.system("open -a Safari")
    elif "chrome" in command:
        os.system("open -a 'Google Chrome'")
    elif "word" in command or "microsoft word" in command:
        os.system("open -a 'Microsoft Word'")
    elif "excel" in command or "microsoft excel" in command:
        os.system("open -a 'Microsoft Excel'")
    else:
        print("Application not recognized. Please try again using your voice command.")

def close_app(command):
    command=command.lower()

    if "Safari" in command:
        os.system("osascript -e 'quit app \"Safari")

        return "closing Safari"
    elif "chrome" in command:
        os.system("osascript -e 'quit app \"Google Chrome\"'")
        return "closing Chrome"
    elif "notepad" in command or "textedit" in command:
        os.system("osascript -e 'quit app \"TextEdit\"'")
        return "closing Notepad"
    elif "calculator" in command:
        os.system("osascript -e 'quit app \"Calculator\"'")
        return "closing Calculator"
    elif "word" in command or "microsoft word" in command:
        os.system("osascript -e 'quit app \"Microsoft Word\"'")
        return "closing Word"
    elif "excel" in command or "microsoft excel" in command:
        os.system("osascript -e 'quit app \"Microsoft Excel\"'")
        return "closing Excel"
    else:
        return "Application not recognized. Please try again using your voice command."
