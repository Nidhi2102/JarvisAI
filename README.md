# 🤖 Jarvis AI – Voice Controlled Smart Assistant

 A powerful AI-based voice assistant built using Python that can understand commands, respond intelligently, and automate tasks like opening apps, searching the web, and managing Google Calendar events.

---

##  Features

* 🎙️ Voice Recognition (Speech-to-Text)
* 🧠 AI Chat using Groq (LLaMA model)
* 🔊 Text-to-Speech Responses
* 🌐 Open Websites (YouTube, Google, Wikipedia, etc.)
* 📅 Google Calendar Integration (Set reminders)
* 📝 Notepad Automation (write using voice)
* ⏰ Real-time Time Updates
* 🔄 Chat Memory + Reset Feature

---

##  Tech Stack

* **Python** 
* **Groq API (LLaMA 3)**
* **SpeechRecognition**
* **pyttsx3 (TTS Engine)**
* **Google OAuth & Calendar API**
* **PyAutoGUI**

---

##  Project Structure

```
JarvisAI/
│── main.py
│── grog.py
│── config.py
│── credentials.example.json
│── token.example.json
│── .env.example
│── requirements.txt
│── README.md
```

---

##  Setup Instructions

### 1️ Clone the Repository

```bash
git clone https://github.com/VedantRajekar/JarvisAI.git
cd JarvisAI
```

---

### 2️ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️ Setup Environment Variables

Create a `.env` file and add:

```
GROQ_API_KEY=your_api_key_here
```

---

### 5️ Setup Google Credentials

* Rename:

```
credentials.example.json → credentials.json
```

* Add your Google OAuth credentials

---

### 6️ Run the Project

```bash
python main.py
```

---

##  Example Commands

* “Open YouTube”
* “Search on Google AI tools”
* “What is the time?”
* “Set a reminder tomorrow at 9 AM”
* “Write in notepad hello world”

---

##  Security Note

* API keys are stored securely using `.env`
* Sensitive files are excluded using `.gitignore`
* Never share your credentials publicly

---

##  Future Improvements

*  Wake word detection (“Hey Jarvis”)
*  GUI Dashboard
*  Mobile Integration
*  Context-aware long conversations

---

##  Author

**Vedant Rajekar**
🚀 Aspiring Software Developer | AI Enthusiast

---

##  Support

If you like this project, don’t forget to ⭐ the repository!

---
