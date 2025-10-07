from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from tools.daily_runner import run_and_notify

_scheduler = None

def start_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Istanbul"))
        trig = CronTrigger(hour=10, minute=0, timezone=pytz.timezone("Europe/Istanbul"))
        _scheduler.add_job(run_and_notify, trig, id="daily_job", replace_existing=True)
        _scheduler.start()

def stop_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
