# System Architecture

```text
                    +------------------------------+
                    | Browser / Elder User         |
                    | Dashboard • Forms • Voice    |
                    +---------------+--------------+
                                    |
                            HTTP / JSON API
                                    |
                    +---------------v--------------+
                    | Flask Application             |
                    | Routes + Reminder Logic       |
                    +-----------+---------+---------+
                                |         |
                       SQLAlchemy         | NLP
                                |         |
                    +-----------v--+   +--v-------------------+
                    | SQLite DB    |   | Local AI Chatbot      |
                    | medications  |   | TF-IDF + Logistic Reg |
                    | dose logs    |   +-----------------------+
                    | wellness     |
                    +-----------+--+
                                |
                    +-----------v-----------+
                    | Analytics / Heuristic  |
                    | adherence + wellness   |
                    +------------------------+

Browser Speech Synthesis API provides multilingual voice output.
A lightweight JSON endpoint is polled by the browser for near-real-time reminder banners and voice alerts.
```

## Main request flow

1. User opens the dashboard.
2. Flask creates any missing reminders for today's active medications.
3. The reminder service updates overdue states to `escalated` after the configured window.
4. The browser polls `/api/reminders` every 30 seconds and speaks new reminders when supported by the browser.
5. Taken/Missed/Snooze actions are persisted in `MedicationLog`.
6. Wellness entries are persisted in `WellnessLog`.
7. Analytics calculates adherence and a transparent demo attention heuristic.
8. Chatbot messages go through TF-IDF feature extraction and Logistic Regression intent classification.
