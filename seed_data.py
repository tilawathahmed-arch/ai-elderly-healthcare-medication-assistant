from datetime import date, datetime, timedelta
from app import create_app, db
from app.models import Medication, MedicationLog, WellnessLog

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    medications = [
        Medication(name="Amlodipine", dosage="5 mg", schedule_time="08:00", instructions="Take after breakfast", language="en", escalation_minutes=30),
        Medication(name="Vitamin D3", dosage="60,000 IU", schedule_time="13:00", instructions="Follow the clinician-approved schedule", language="hi", escalation_minutes=45),
        Medication(name="Metformin", dosage="500 mg", schedule_time="20:00", instructions="Take with food if prescribed", language="te", escalation_minutes=30),
    ]
    db.session.add_all(medications)
    db.session.flush()

    now = datetime.now()
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    db.session.add_all([
        MedicationLog(medication_id=medications[0].id, scheduled_for=start_today + timedelta(hours=8), status="taken", action_time=now),
        MedicationLog(medication_id=medications[1].id, scheduled_for=start_today + timedelta(hours=13), status="missed", action_time=now),
        MedicationLog(medication_id=medications[2].id, scheduled_for=start_today + timedelta(hours=20), status="pending"),
    ])

    samples = [
        (0, 4, 7.5, 2, 4, 128, 82, "Felt energetic."),
        (1, 4, 7.0, 3, 4, 130, 84, "Mild knee discomfort."),
        (2, 3, 6.5, 4, 3, 134, 86, "Slept a little less."),
        (3, 4, 7.8, 2, 4, 126, 80, "Good appetite."),
        (4, 5, 8.0, 1, 5, 124, 79, "Good day."),
    ]
    for days_ago, mood, sleep, pain, appetite, sys, dia, notes in samples:
        db.session.add(WellnessLog(log_date=date.today() - timedelta(days=days_ago), mood=mood, sleep_hours=sleep, pain=pain, appetite=appetite, systolic=sys, diastolic=dia, notes=notes))

    db.session.commit()
    print("Database reset and realistic sample data inserted.")
