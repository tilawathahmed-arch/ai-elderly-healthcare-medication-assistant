from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from app import create_app, db
from config import Config
from app.models import Medication, MedicationLog, WellnessLog
from app.reminder import action_on_log, ensure_today_logs


def make_app(tmp_path):
    class TempConfig(Config):
        TESTING = True
        SECRET_KEY = "test-key"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(tmp_path) / 'test.db'}"
    return create_app(TempConfig)


def test_pages_and_crud():
    with TemporaryDirectory() as tmp:
        app = make_app(tmp)
        client = app.test_client()
        assert client.get('/').status_code == 200
        assert client.get('/medications').status_code == 200
        assert client.get('/wellness').status_code == 200
        assert client.get('/analytics').status_code == 200
        assert client.get('/chat').status_code == 200
        response = client.post('/medications/add', data={
            'name': 'DemoMed', 'dosage': '10 mg', 'schedule_time': '09:00',
            'language': 'en', 'escalation_minutes': '30', 'instructions': 'After food'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            med = Medication.query.filter_by(name='DemoMed').first()
            assert med is not None
            client.post(f'/medications/{med.id}/edit', data={
                'name': 'DemoMed2', 'dosage': '20 mg', 'schedule_time': '10:00',
                'language': 'te', 'escalation_minutes': '60', 'instructions': 'Updated'
            })
            assert Medication.query.filter_by(name='DemoMed2').first() is not None


def test_wellness_and_reminder_actions():
    with TemporaryDirectory() as tmp:
        app = make_app(tmp)
        client = app.test_client()
        client.post('/wellness', data={
            'log_date': '2026-09-25', 'mood': '4', 'sleep_hours': '7.5', 'pain': '2', 'appetite': '4',
            'systolic': '120', 'diastolic': '80', 'notes': 'Feeling good'
        })
        with app.app_context():
            assert WellnessLog.query.count() == 1
            med = Medication(name='Test', dosage='5 mg', schedule_time=datetime.now().strftime('%H:%M'))
            db.session.add(med); db.session.commit()
            ensure_today_logs()
            log = MedicationLog.query.filter_by(medication_id=med.id).first()
            assert log is not None
            action_on_log(log.id, 'taken')
            assert MedicationLog.query.get(log.id).status == 'taken'


def test_chat_api():
    with TemporaryDirectory() as tmp:
        app = make_app(tmp)
        client = app.test_client()
        response = client.post('/chat', data={'message': 'I feel dizzy'})
        assert response.status_code == 200
        assert b"dizzy" in response.data.lower() or b"urgent" in response.data.lower()
