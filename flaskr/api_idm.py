from flask         import Blueprint
from flask         import request, jsonify
from flaskr        import db
from flaskr.models import Person, WorkRec
from datetime      import datetime
import json

bp = Blueprint('api_idm', __name__, url_prefix="/api/idm")

@bp.route('/<idm>',methods=['GET'])
def get_idm(idm):
    person = Person.query.filter_by(idm=idm).first()
    if person == None:
        return jsonify({"name": "該当者無し"}), 404
    result = dict(
        name=person.name
    )
    return jsonify(result), 200

@bp.route('/<idm>',methods=['POST'])
def post_idm(idm):
    person = Person.query.filter_by(idm=idm).first()
    if person == None:
        return jsonify({"message": "Not Found!"}), 404
    now=datetime.now()
    yymm=now.strftime('%Y%m')
    dd=now.day
    hhmm=now.strftime('%H:%M')
    workrec=WorkRec.query.filter_by(
        person_id=person.id, yymm=yymm, dd=dd
    ).first()
    creation=False
    if workrec == None:
        creation = False
        workrec = WorkRec(person_id=person.id, yymm=yymm,dd=dd)
    
    db.session.add(workrec)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({}), 500
    if creation:
        result = dict(
            work_in = workrec.work_in
        )
        return jsonify({}), 201
    result = dict(
        work_in  = workrec.work_in,
        work_out = workrec.work_out
    )
    return jsonify(result), 200