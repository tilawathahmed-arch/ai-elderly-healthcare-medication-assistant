from datetime import date, datetime, timedelta
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from . import db
from .chatbot import get_response
from .models import Medication, MedicationLog, WellnessLog
from .reminder import action_on_log, refresh_statuses
from .services.analytics import medication_adherence, wellness_summary

main = Blueprint("main", __name__)


@main.app_context_processor
def inject_globals():
    return {"current_year": datetime.now().year}


def _today_range():
    start = datetime.combine(date.today(), datetime.min.time())
    return start, start + timedelta(days=1)


@main.route("/")
def index():
    refresh_statuses()
    start, end = _today_range()
    logs = MedicationLog.query.filter(
        MedicationLog.scheduled_for >= start,
        MedicationLog.scheduled_for < end,
    ).order_by(MedicationLog.scheduled_for.asc()).all()
    return render_template(
        "index.html", logs=logs, wellness=wellness_summary(), adherence=medication_adherence()
    )


@main.route("/medications")
def medications():
    refresh_statuses()
    start, end = _today_range()
    meds = Medication.query.order_by(Medication.active.desc(), Medication.schedule_time.asc()).all()
    logs = MedicationLog.query.filter(
        MedicationLog.scheduled_for >= start,
        MedicationLog.scheduled_for < end,
    ).order_by(MedicationLog.scheduled_for.asc()).all()
    return render_template("medications.html", medications=meds, logs=logs)


@main.route("/medications/add", methods=["GET", "POST"])
def add_medication():
    if request.method == "POST":
        med = Medication(
            name=request.form.get("name", "").strip(),
            dosage=request.form.get("dosage", "").strip(),
            schedule_time=request.form.get("schedule_time", ""),
            instructions=request.form.get("instructions", "").strip(),
            language=request.form.get("language", "en"),
            escalation_minutes=int(request.form.get("escalation_minutes", 30)),
        )
        if not med.name or not med.dosage or not med.schedule_time:
            flash("Please complete the required medication fields.", "error")
            return render_template("medication_form.html", medication=None)
        db.session.add(med)
        db.session.commit()
        flash("Medication added successfully.", "success")
        return redirect(url_for("main.medications"))
    return render_template("medication_form.html", medication=None)


@main.route("/medications/<int:med_id>/edit", methods=["GET", "POST"])
def edit_medication(med_id):
    med = Medication.query.get_or_404(med_id)
    if request.method == "POST":
        med.name = request.form.get("name", "").strip()
        med.dosage = request.form.get("dosage", "").strip()
        med.schedule_time = request.form.get("schedule_time", "")
        med.instructions = request.form.get("instructions", "").strip()
        med.language = request.form.get("language", "en")
        med.escalation_minutes = int(request.form.get("escalation_minutes", 30))
        db.session.commit()
        flash("Medication updated.", "success")
        return redirect(url_for("main.medications"))
    return render_template("medication_form.html", medication=med)


@main.route("/medications/<int:med_id>/toggle", methods=["POST"])
def toggle_medication(med_id):
    med = Medication.query.get_or_404(med_id)
    med.active = not med.active
    db.session.commit()
    flash(f"{med.name} is now {'active' if med.active else 'inactive'}.", "success")
    return redirect(url_for("main.medications"))


@main.route("/medications/<int:med_id>/delete", methods=["POST"])
def delete_medication(med_id):
    med = Medication.query.get_or_404(med_id)
    db.session.delete(med)
    db.session.commit()
    flash("Medication removed.", "success")
    return redirect(url_for("main.medications"))


@main.route("/reminders/<int:log_id>/<action>", methods=["POST"])
def reminder_action(log_id, action):
    if action not in {"taken", "missed", "snooze"}:
        flash("Unsupported reminder action.", "error")
        return redirect(url_for("main.medications"))
    action_on_log(log_id, action)
    flash(f"Reminder marked as {action}.", "success")
    return redirect(request.referrer or url_for("main.medications"))


@main.route("/api/reminders")
def reminder_api():
    refresh_statuses()
    now = datetime.now()
    today_start, today_end = _today_range()
    upcoming_start = now - timedelta(minutes=2)
    upcoming_end = now + timedelta(minutes=2)
    logs = MedicationLog.query.join(Medication).filter(
        MedicationLog.scheduled_for >= today_start,
        MedicationLog.scheduled_for < today_end,
        MedicationLog.status.in_(["pending", "escalated"]),
        Medication.active.is_(True),
    ).all()
    # Return reminders that are currently due/escalated, plus reminders due in the next 2 minutes.
    logs = [
        log for log in logs
        if log.status == "escalated" or (upcoming_start <= log.scheduled_for <= upcoming_end)
    ]
    return jsonify({
        "server_time": now.isoformat(timespec="seconds"),
        "reminders": [
            {
                "id": log.id,
                "medicine": log.medication.name,
                "dosage": log.medication.dosage,
                "time": log.scheduled_for.strftime("%I:%M %p"),
                "language": log.medication.language,
                "instructions": log.medication.instructions,
                "status": log.status,
            }
            for log in logs
        ],
    })


@main.route("/wellness", methods=["GET", "POST"])
def wellness():
    if request.method == "POST":
        try:
            log = WellnessLog(
                log_date=date.fromisoformat(request.form["log_date"]),
                mood=int(request.form["mood"]),
                sleep_hours=float(request.form["sleep_hours"]),
                pain=int(request.form["pain"]),
                appetite=int(request.form["appetite"]),
                systolic=int(request.form["systolic"]) if request.form.get("systolic") else None,
                diastolic=int(request.form["diastolic"]) if request.form.get("diastolic") else None,
                notes=request.form.get("notes", "").strip(),
            )
            db.session.add(log)
            db.session.commit()
            flash("Wellness entry saved.", "success")
            return redirect(url_for("main.wellness"))
        except (ValueError, TypeError):
            flash("Please check the wellness values and try again.", "error")
    logs = WellnessLog.query.order_by(WellnessLog.log_date.desc(), WellnessLog.id.desc()).limit(30).all()
    return render_template("wellness.html", logs=logs, today=date.today().isoformat())


@main.route("/analytics")
def analytics():
    refresh_statuses()
    return render_template(
        "analytics.html",
        summary=wellness_summary(),
        adherence=medication_adherence(),
        recent_wellness=WellnessLog.query.order_by(WellnessLog.log_date.desc()).limit(7).all(),
        recent_logs=MedicationLog.query.order_by(MedicationLog.scheduled_for.desc()).limit(20).all(),
    )


@main.route("/chat", methods=["GET", "POST"])
def chat():
    result = None
    message = ""
    if request.method == "POST":
        message = request.form.get("message", "")
        result = get_response(message)
    return render_template("chat.html", result=result, message=message)
