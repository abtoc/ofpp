from flaskr        import app,db,celery
from flaskr.models import WorkRec
from datetime               import datetime
from dateutil.relativedelta import relativedelta

@celery.task
def destroy_workrec():
    app.logger.info('Destroy WorkRec')
    now = datetime.now()
    now = now - relativedelta(years=5)
    yymm = now.strftime('%Y%m')
    workrecs = WorkRec.query.filter(WorkRec.yymm<yymm).all()
    for workrec in workrecs:
        db.session.delete(workrec)
        db.session.commit()
