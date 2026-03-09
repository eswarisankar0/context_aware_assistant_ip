from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_reminder(reminder):

    if not reminder["time"]:
        return

    run_time = datetime.strptime(reminder["time"], "%Y-%m-%d %H:%M:%S")

    scheduler.add_job(
        notify,
        'date',
        run_date=run_time,
        args=[reminder]
    )

def notify(reminder):
    print(f"\n🔔 REMINDER: {reminder['task']}\n")