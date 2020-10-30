from flask import Blueprint, jsonify
from datetime import datetime
from uuid import uuid4
from app.services.aws.organization import Organization
from app.models.db.account import Account
from app.models.db.db import db
import os

accounts = Blueprint('accounts', __name__)

def _delete_old_accounts(new_job_uuid):
    old_accounts = Account.query.filter(Account.job_uuid!=new_job_uuid, Account.foreign==False).all()
    for old_account in old_accounts:
        db.session.delete(old_account)
    db.session.commit()
    

@accounts.route('/', methods=['POST'])
def post():
#    if os.environ.get('SCOPE') == 'single-account':
#        return {"msg": "This endpoint is of no use when SCOPE is local, please read the documentation for more info"}, 417
    job_uuid= datetime.now().strftime('%Y%m%d-%H-%M%S-') + str(uuid4())
    try:
        org = Organization()
        accounts = org.get_accounts()
        for uuid, name in accounts.items():
            acc = Account.find_or_create(uuid=uuid)
            acc.job_uuid = job_uuid
            acc.name = name
            acc.updated_at = datetime.now()
            db.session.add(acc)
        db.session.commit()
        _delete_old_accounts(job_uuid)
        return {"message": "Accounts job ran successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 503 # TODO: See if we need to categorize Exceptions
    finally:
        db.session.close()
