# AI-Powered Elderly Healthcare and Medication Assistance System

An accessible Flask + SQLite project that combines **medication management, adaptive reminders, voice assistance, wellness tracking, analytics, and an AI/NLP chatbot** for an elderly-care demonstration.

> **Important:** This is an educational software project. It is not a medical device, diagnostic system, emergency service, or substitute for a doctor, pharmacist, or professional caregiver.

## ✨ Features

- 🤖 **AI healthcare chatbot** using a local TF-IDF + Logistic Regression intent classifier
- 💊 **Medication management** with add/edit/enable/disable/delete operations
- ⏰ **Intelligent reminders** with Taken, Missed, and 10-minute Snooze actions
- 🚨 **Adaptive escalation** when a reminder remains unhandled beyond its configured window
- 🔊 **Voice notifications** using the browser Web Speech API with English/Hindi/Telugu language tags
- ❤️ **Wellness tracking** for mood, sleep, pain, appetite, blood pressure, and notes
- 📊 **Analytics dashboard** for adherence and wellness insights
- 🗃️ **SQLite + SQLAlchemy** persistent storage
- 📱 **Responsive UI** designed to stay simple and readable on desktop/mobile
- 🧪 **Automated tests** for checking the application
- 🌱 **Seed data** for a ready-made demonstration

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite, Flask-SQLAlchemy |
| AI / ML | scikit-learn, TF-IDF, Logistic Regression |
| Model persistence | joblib |
| Frontend | HTML5, CSS3, JavaScript |
| Voice | Browser Speech Synthesis API |
| Testing | pytest |

## 📁 Project Structure

```text
elderly_healthcare_ai/
├── app/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── models.py
│   ├── reminder.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── analytics.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── medications.html
│       ├── medication_form.html
│       ├── wellness.html
│       ├── analytics.html
│       └── chat.html
├── data/
│   └── intents.json
├── docs/
│   ├── ARCHITECTURE.md
│   └── PROJECT_GUIDE.md
├── ml/
│   ├── model/
│   │   ├── chatbot_pipeline.joblib
│   │   └── responses.json
│   └── train_chatbot.py
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
├── run_linux.sh
├── run_windows.bat
├── seed_data.py
├── train_model.py
└── README.md
```

## 🚀 Installation

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Run the project

Train (or retrain) the chatbot:

```bash
python train_model.py
```

Create the demo database and sample records:

```bash
python seed_data.py
```

Start the web app:

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

The SQLite database is created automatically as `elderly_healthcare.db`.

## 🧪 Run tests

```bash
pytest -q
```


## 🧠 How the AI works

The chatbot is intentionally lightweight and explainable:

```text
User message
    ↓
TF-IDF Vectorizer
    ↓
Logistic Regression
    ↓
Predicted intent + confidence
    ↓
Predefined safe response
```

The training examples and response templates live in:

```text
data/intents.json
```

Retrain after changing the dataset:

```bash
python train_model.py
```

## 🔔 Reminder logic

Each active medication has a scheduled time and an escalation window.

- At the scheduled time, the dose becomes due.
- **Taken** records successful adherence.
- **Missed** records a missed dose.
- **Snooze** moves the reminder forward by 10 minutes.
- If an active, unhandled reminder passes its escalation window, it becomes **Escalated**.
- The browser checks `/api/reminders` every 30 seconds, shows a reminder banner, and reads new reminders aloud when Speech Synthesis is available.

## 🌐 Voice support

The app requests these browser language tags:

- English: `en-IN`
- Hindi: `hi-IN`
- Telugu: `te-IN`

Exact voice availability depends on the operating system and browser.

## 📊 Analytics logic

### Medication adherence

```text
Adherence % = Taken doses / (Taken + Missed doses) × 100
```

### Wellness attention indicator

A transparent demo heuristic adds attention points for low average sleep, higher average pain, low average mood, and low average appetite. It is **not** a validated medical risk model.

## 🔐 Configuration

Copy `.env.example` to `.env` and set a stronger secret key for development deployments. For production, also place the app behind a proper WSGI server and add authentication, authorization, HTTPS, database backups, audit logs, and privacy controls.

## 🧑‍💻 GitHub upload

Create a new GitHub repository and run:

```bash
git init
git add .
git commit -m "Initial commit: ElderCare AI"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

### Suggested GitHub repository name

`ai-elderly-healthcare-medication-assistant`

### Suggested repository description

`AI-powered elderly healthcare assistance system with medication reminders, voice alerts, wellness tracking, analytics, and an NLP chatbot using Flask and machine learning.`


