from statistics import mean
from ..models import MedicationLog, WellnessLog


def medication_adherence(logs=None):
    logs = logs if logs is not None else MedicationLog.query.all()
    handled = [x for x in logs if x.status in {"taken", "missed"}]
    if not handled:
        return 0.0
    taken = sum(1 for x in handled if x.status == "taken")
    return round((taken / len(handled)) * 100, 1)


def wellness_summary(logs=None):
    logs = logs if logs is not None else WellnessLog.query.order_by(WellnessLog.log_date.asc()).all()
    if not logs:
        return {
            "avg_mood": 0, "avg_sleep": 0, "avg_pain": 0,
            "avg_appetite": 0, "latest": None, "risk": "No data", "risk_points": 0
        }

    avg_mood = round(mean(x.mood for x in logs), 2)
    avg_sleep = round(mean(x.sleep_hours for x in logs), 2)
    avg_pain = round(mean(x.pain for x in logs), 2)
    avg_appetite = round(mean(x.appetite for x in logs), 2)

    risk_points = 0
    if avg_sleep < 6:
        risk_points += 1
    if avg_pain >= 7:
        risk_points += 2
    elif avg_pain >= 4:
        risk_points += 1
    if avg_mood <= 2:
        risk_points += 1
    if avg_appetite <= 2:
        risk_points += 1

    if risk_points >= 4:
        risk = "High attention"
    elif risk_points >= 2:
        risk = "Needs attention"
    else:
        risk = "Stable"

    return {
        "avg_mood": avg_mood, "avg_sleep": avg_sleep, "avg_pain": avg_pain,
        "avg_appetite": avg_appetite, "latest": logs[-1],
        "risk": risk, "risk_points": risk_points
    }
