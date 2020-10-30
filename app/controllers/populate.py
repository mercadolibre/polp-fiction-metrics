from datetime import datetime
from uuid import uuid4
import os

from flask import Blueprint
from app.models.db.account import Account
from app.models.updaters.policy_updater import PolicyUpdater
from app.models.updaters.role_updater import RoleUpdater
from app.models.updaters.user_updater import UserUpdater
from app.models.updaters.access_updater import AccessUpdater
from app.services.aws.iam import IAM
from app.config import POLP_FICTION_MASTER_ACCOUNT

# Cleaner imports
from app.models.db.permission import Permission
from app.models.db.policy import Policy
from app.models.db.role import Role
from app.models.db.user import User
from app.models.db.db import db

populates = Blueprint('populates', __name__)


def _delete_old_entity(entity, new_job_uuid):
    try:
        old_entities = entity.query.filter(entity.job_uuid!=new_job_uuid)
        for old_entity in old_entities:
            db.session.delete(old_entity)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()


def _delete_old_entities(new_job_uuid):
    _delete_old_entity(Role, new_job_uuid)
    _delete_old_entity(User, new_job_uuid)
    _delete_old_entity(Policy, new_job_uuid)
    _delete_old_entity(Permission, new_job_uuid)

def get_accounts():
    job_uuid = datetime.now().strftime('%Y%m%d-%H-%M%S-') + str(uuid4())
    accounts = Account.query.filter_by(foreign=False).all()
    if os.environ.get('SCOPE') == 'single-account':
        acc = Account.find_or_create(POLP_FICTION_MASTER_ACCOUNT)
        db.session.add(acc)
        db.session.commit()
        accounts = [acc]
    return accounts, job_uuid


@populates.route('/', methods=['POST'])
def post():
    try:
        accounts, job_uuid = get_accounts()
        for acc in accounts:
            iam = IAM(acc)
            policy_updater = PolicyUpdater(iam, job_uuid)
            user_updater = UserUpdater(iam, job_uuid)
            role_updater = RoleUpdater(iam, job_uuid)
            access_updater = AccessUpdater(iam, job_uuid)
            policy_updater.update_policies()
            role_updater.update_roles()
            user_updater.update_users()
            access_updater.update_policies_last_access()
        _delete_old_entities(job_uuid)
        return {"msg": "Population job ran successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
