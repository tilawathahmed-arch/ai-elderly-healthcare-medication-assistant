from datetime import datetime
from . import db


class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(120), nullable=False)
    schedule_time = db.Column(db.String(5), nullable=False)
    instructions = db.Column(db.String(255), default="")
    language = db.Column(db.String(20), default="en")
    escalation_minutes = db.Column(db.Integer, default=30)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logs = db.relationship(
        "MedicationLog", backref="medication", lazy=True,
        cascade="all, delete-orphan"
    )


class MedicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medication.id"), nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default="pending")
    action_time = db.Column(db.DateTime, nullable=True)
    snooze_count = db.Column(db.Integer, default=0)


class WellnessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_date = db.Column(db.Date, nullable=False)
    mood = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    pain = db.Column(db.Integer, nullable=False)
    appetite = db.Column(db.Integer, nullable=False)
    systolic = db.Column(db.Integer, nullable=True)
    diastolic = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
