from textblob import TextBlob

def get_mood(text):
    polarity = TextBlob(text).sentiment.polarity    
    if polarity > 0.1:
        return "happy"
    elif polarity < -0.1:
        return "sad"
    else:
        return "neutral"