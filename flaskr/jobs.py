from flaskr        import db,scheduler
from flaskr.models import WorkRec
from datetime               import datetime
from dateutil.relativedelta import relativedelta

def destroy_workrec():
    now = datetime.now()
    now = now - relativedelta(years=2)
    yymm = now.strftime('%Y%m')
    workrecs = WorkRec.query.filter(WorkRec.yymm<yymm).all()
    for workrec in workrecs:
        db.session.delete(workrec)
        db.session.commit()

scheduler.add_job(
    'job1',
    destroy_workrec,
    trigger="cron",
    hour=12,
    minute=34,
    second=0
)
