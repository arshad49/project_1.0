import edge_tts
import os
import asyncio
import subprocess
async def speak_edge(text, voice='en-US-AriaNeural'):
    # Ensure text is a string
    if not isinstance(text, str):
        raise ValueError("The 'text' parameter must be a string.")
    
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save("speech.mp3")
    
    # Play the audio file
    os.system("afplay speech.mp3")  # For macOS, use 'afplay' to play a file
    # Alternatively, you can use subprocess
    # subprocess.call(["afplay", "speech.mp3"])
def speak(text, voice='en-US-AriaNeural', style="general"):
    # Ensure text is a string before calling the async function
    if not isinstance(text, str):
        raise ValueError("The 'text' parameter must be a string.")
    
    print(f"Speaking text: {text}")  # Debugging information
    asyncio.run(speak_edge(text, voice=voice))