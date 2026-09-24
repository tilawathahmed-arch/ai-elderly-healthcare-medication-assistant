# Project Guide / Viva Notes

## Problem Statement

Senior citizens can benefit from simpler medication schedules, reminders, voice assistance, and an easy wellness journal. The project combines those functions with a lightweight NLP assistant and a dashboard for basic analytics.

## Modules

### 1. Medication Management
Add, edit, enable/disable, and delete medications. Each medicine stores a dose, time, reminder language, instructions, and escalation window.

### 2. Medication Reminder & Escalation
The app creates a daily reminder record for active medicines. Users can mark a reminder as Taken, Missed, or Snooze. After the escalation window, an unhandled reminder is displayed as Escalated.

### 3. Voice Assistance
The browser Speech Synthesis API reads reminders and chatbot responses aloud. The project uses `en-IN`, `hi-IN`, and `te-IN` language tags where the device/browser has supporting voices.

### 4. AI / NLP Chatbot
Training data is stored in `data/intents.json`.

Pipeline:

`Text → TF-IDF Vectorizer → Logistic Regression → Intent → Safe Response`

The chatbot is deliberately restricted to predefined informational responses so that the project is easy to explain and does not pretend to be a clinician.

### 5. Wellness Tracking
Daily values include mood, sleep, pain, appetite, optional blood pressure, and notes.

### 6. Analytics
The dashboard shows medication adherence, wellness averages, and a rule-based attention indicator. The indicator is educational only and must not be interpreted as clinical diagnosis.

## Demo Steps

1. Run `python train_model.py`.
2. Run `python seed_data.py` for sample data.
3. Run `python run.py`.
4. Open `http://127.0.0.1:5000`.
5. Add a medication and inspect today's reminder.
6. Use Taken/Missed/Snooze.
7. Try the voice button and enable browser audio permissions if needed.
8. Open AI Assistant and try "I feel dizzy" or "How can I sleep better?".
9. Record a wellness entry.
10. Review Analytics.

## Limitations

- This is an academic/demo project, not a medical device.
- No hospital/EHR integration is included.
- No real SMS, WhatsApp, phone-call, or caregiver push service is included.
- Voice output depends on browser/device support.
- The chatbot is not a general medical LLM and may not understand out-of-domain questions.
- The attention indicator is a transparent heuristic, not a validated risk model.
- Authentication and role-based access are not included in this single-user demo.
