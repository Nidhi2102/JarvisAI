import os
import webbrowser
import datetime
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from groq import Groq

# ========== INITIAL SETUP ==========
engine = pyttsx3.init()
engine.setProperty('rate', 175)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chatStr = ""


# ---------- FUNCTIONS ----------
def say(text):
    """Make Jarvis speak"""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    """Take voice input from user"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""


def chat(query):
    """Chat concisely using Groq Llama model"""
    global chatStr
    chatStr += f"User: {query}\nJarvis: "

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system",
             "content": "You are Jarvis, a concise AI assistant. Always reply in under 3 short sentences."},
            {"role": "user", "content": query},
        ]
    )

    reply = response.choices[0].message.content.strip()
    chatStr += f"{reply}\n"
    print(f"Jarvis: {reply}")
    say(reply)
    return reply


def ai(prompt):
    """Handle AI-based questions or tasks"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system",
             "content": "You are Jarvis, a concise and helpful AI assistant. Respond in under 3 short sentences."},
            {"role": "user", "content": prompt},
        ]
    )
    reply = response.choices[0].message.content.strip()
    print("AI:", reply)
    say(reply)
    return reply


# ---------- MAIN PROGRAM ----------
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Welcome to Jarvis Artificial Intelligence")

    while True:
        query = takeCommand().lower()

        if not query:
            continue

        # --- Website Shortcuts ---
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
        ]
        site_opened = False
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}, sir.")
                webbrowser.open(site[1])
                site_opened = True
                break
        if site_opened:
            continue

        # --- Music ---
        if "open music" in query or "play music" in query:
            say("Playing music, sir.")
            musicPath = "C:\\Users\\Asus\\Music\\song.mp3"  # change path
            os.startfile(musicPath)
            continue

        # --- Time ---
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")
            continue

        # --- Facetime / Passky placeholders ---
        elif "open facetime" in query:
            say("Facetime is not available on Windows.")
            continue

        elif "open pass" in query:
            say("Passky app is not available on Windows.")
            continue

        # --- AI Mode ---
        elif "using artificial intelligence" in query:
            ai(prompt=query)
            continue

        # --- Quit Command ---
        elif "jarvis quit" in query or "exit" in query:
            say("Goodbye sir!")
            break

        # --- Reset Chat ---
        elif "reset chat" in query:
            chatStr = ""
            say("Chat memory cleared.")
            continue

        # --- General Chat (short answers) ---
        else:
            chat(query)
