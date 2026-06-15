import webbrowser

def open_website(command):
    urls = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",
        "whatsapp": "https://web.whatsapp.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "linkedin": "https://www.linkedin.com",
        "twitter": "https://twitter.com",
        "chatgpt": "https://chat.openai.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "weather": "https://www.weather.com",
        "maps": "https://www.google.com/maps",
        "news": "https://news.google.com",
        "drive": "https://drive.google.com",
        "calendar": "https://calendar.google.com"
    }

    for key in urls:
        if key in command:
            webbrowser.open(urls[key])
            print(f"Opening {key.capitalize()}...")
            return

    print("Sorry, I couldn't find a matching website for your command.")


