from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from app.models.db.db import db
from app.models.db.permission import Permission
from app.models.db.policy import Policy

class AccessUpdater():

    def __init__(self, iam, job_uuid):
        self.iam = iam
        self.job_uuid = job_uuid
        self.account = iam.get_account()

    def _get_policies(self):
        policies = Policy.query.filter_by(job_uuid=self.job_uuid, account_id=self.account.id).all()
        return policies

    def _set_last_authenticated(self, access_details, policies):
            for policy in policies:
                policy_access_data = access_details.get(policy.arn)
                for p in policy.permissions:
                    permission_access_data = policy_access_data.get(p.service.name) if policy_access_data else None
                    last_access_epoch_time = permission_access_data.get('LastAuthenticated') if permission_access_data else None
                    p.last_used = last_access_epoch_time if last_access_epoch_time and last_access_epoch_time != 0 else None
                    p.last_auth_entity = permission_access_data.get('LastAuthenticatedEntity') if permission_access_data else None
                yield(policy)

    def update_policies_last_access(self):
        policies = self._get_policies()
        policies_arn = [ policy.arn for policy in policies ]
        access_details = self.iam.get_last_access_data_for_arns(policies_arn)
        try:
            for policy in self._set_last_authenticated(access_details, policies):
                db.session.add(policy)
                db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error committing Users to the Database: \n {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()
