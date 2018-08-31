from flaskr import app, db, celery
from flaskr.models import Person, WorkRec
from datetime import datetime
from dateutil.relativedelta import relativedelta

@celery.task
def enabled_workrec(person_id, yymm):
    app.logger.info('Enabled WorkRec person_id={} yymm={}'.format(person_id,yymm))
    person = Person.get(person_id)
    if person.staff:
        return
    yy     = int(yymm[:4])
    mm     = int(yymm[4:])
    first  = datetime(yy, mm, 1)
    last   = first + relativedelta(months=1) - relativedelta(days=1)
    last   = last.day - 8
    workrecs = WorkRec.get_yymm(person_id, yymm)
    count = 0
    for workrec in workrecs:
        if workrec.value is None:
            workrec.value = None
        else:
            count = count + 1
            if count <= last:
                workrec.enabled = True
            else:
                workrec.enabled = False
        db.session.add(workrec)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e.message)
