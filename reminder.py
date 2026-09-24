from datetime import datetime, timedelta
from . import db
from .models import Medication, MedicationLog


SNOOZE_MINUTES = 10


def today_at(time_str: str):
    now = datetime.now()
    hour, minute = [int(part) for part in time_str.split(":")]
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def ensure_today_logs():
    """Create one reminder record per active medication for today."""
    today = datetime.now().date()
    created = 0
    for med in Medication.query.filter_by(active=True).all():
        scheduled = today_at(med.schedule_time)
        existing = MedicationLog.query.filter_by(
            medication_id=med.id, scheduled_for=scheduled
        ).first()
        if existing is None:
            db.session.add(
                MedicationLog(medication_id=med.id, scheduled_for=scheduled, status="pending")
            )
            created += 1
    if created:
        db.session.commit()
    return created


def refresh_statuses():
    ensure_today_logs()
    now = datetime.now()
    changed = False
    for log in MedicationLog.query.join(Medication).filter(Medication.active.is_(True)).all():
        if log.status in {"taken", "missed"}:
            continue
        med = log.medication
        escalation_at = log.scheduled_for + timedelta(minutes=med.escalation_minutes)
        if now >= escalation_at:
            if log.status != "escalated":
                log.status = "escalated"
                changed = True
        elif now >= log.scheduled_for and log.status == "pending":
            # The dashboard treats this state as due based on the scheduled time.
            pass
    if changed:
        db.session.commit()


def action_on_log(log_id: int, action: str):
    log = MedicationLog.query.get_or_404(log_id)
    if action == "taken":
        log.status = "taken"
        log.action_time = datetime.now()
    elif action == "missed":
        log.status = "missed"
        log.action_time = datetime.now()
    elif action == "snooze":
        if log.status in {"taken", "missed"}:
            return log
        log.snooze_count += 1
        log.scheduled_for = max(log.scheduled_for, datetime.now()) + timedelta(minutes=SNOOZE_MINUTES)
        log.status = "pending"
    else:
        raise ValueError("Unsupported reminder action")
    db.session.commit()
    return log
