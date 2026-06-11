import speech_recognition as sr
import webbrowser
import pyttsx3
import random
from groq import Groq
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
import pyautogui
import time
import subprocess

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def write_in_notepad():
    say("What should I write, sir?")
    note_text = takeCommand()

    if not note_text.strip():
        say("I didn’t catch that. Please try again.")
        return

    say("Opening Notepad...")
    # Open Notepad using subprocess
    subprocess.Popen(["notepad.exe"])
    time.sleep(2)  # Wait for Notepad to fully open

    # Type the text slowly to simulate typing
    pyautogui.typewrite(note_text, interval=0.05)
    say("Done. I've written it in Notepad.")

def add_to_google_calendar(reminder):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': reminder,
        'start': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(minutes=2)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(minutes=32)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Reminder added: {event.get('htmlLink')}")
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chatStr = ""

# ---------- SPEAK FUNCTION ----------
def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # [0]=male, [1]=female
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()


# ---------- CHAT FUNCTION ----------
def chat(query):
    global chatStr
    chatStr += f"You: {query}\nJarvis: "

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=100,
        messages=[
            {"role": "system",
             "content": "You are Jarvis, a concise and friendly AI. Respond in 2–3 sentences maximum."},
            {"role": "user", "content": query}
        ]
    )

    text = response.choices[0].message.content
    chatStr += text + "\n"
    print(f"Jarvis: {text}")
    say(text)
    return text


# ---------- AI PROMPT FUNCTION ----------
def ai(prompt):
    text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    output_text = response.choices[0].text
    say(output_text)
    text += output_text

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # Save response to a file
    filename = f"Openai/prompt-{random.randint(1, 999999)}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


# ---------- LISTEN FUNCTION ----------
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception:
            say("Sorry, I didn't catch that.")
            return ""

def add_to_google_calendar_custom(reminder, reminder_time):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': reminder,
        'start': {
            'dateTime': reminder_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (reminder_time + datetime.timedelta(minutes=30)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Reminder added: {event.get('htmlLink')}")


# ---------- MAIN PROGRAM ----------
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Welcome to Jarvis Artificial Intelligence")

    while True:
        print("Listening...")
        query = takeCommand().lower()

        # --- Website Shortcuts ---
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
        ]
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                break

        # --- YouTube Search ---
        if "search on youtube" in query:
            search_term = query.replace("search on youtube", "").strip()
            if search_term:
                say(f"Searching {search_term} on YouTube")
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
            continue

        # --- Google Search ---
        elif "search on google" in query:
            search_term = query.replace("search on google", "").strip()
            if search_term:
                say(f"Searching {search_term} on Google")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            continue

        # --- Google Calendar Reminder ---
        elif 'reminder' in query or 'calendar' in query:
            say("What should I remind you about?")
            reminder_text = takeCommand()

            say("When should I remind you? You can say something like 'tomorrow at 9 AM' or 'on 5th November at 6 PM'.")
            time_text = takeCommand()

            try:
                import dateparser

                reminder_time = dateparser.parse(time_text)
                if reminder_time is None:
                    say("Sorry, I couldn’t understand the time. I’ll set it 2 minutes from now.")
                    reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=2)

                add_to_google_calendar_custom(reminder_text, reminder_time)
                say(f"Reminder set for {reminder_time.strftime('%A, %I:%M %p')}")
            except Exception as e:
                print(e)
                say("Sorry, I couldn’t set that reminder.")


        # --- Music ---
        elif "open music" in query:
            musicPath = "C:\\Users\\Asus\\Downloads\\Songs"  # change path if needed
            os.startfile(musicPath)

        # --- Time ---
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes.")

        # --- Extra Apps (optional) ---
        elif "open notepad" in query or "write in notepad" in query:
            write_in_notepad()

        # --- AI Prompt Feature ---
        elif "using artificial intelligence" in query:
            ai(prompt=query)

        # --- Quit Command ---
        elif "jarvis quit" in query or "exit" in query:
            say("Goodbye sir!")
            break

        # --- Reset Chat ---
        elif "reset chat" in query:
            chatStr = ""
            say("Chat memory cleared.")

        # --- Chat Mode ---
        elif query.strip() != "":
            print("Chatting...")
            chat(query)
