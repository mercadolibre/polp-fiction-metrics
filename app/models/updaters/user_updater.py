from datetime import datetime

from policyuniverse.policy import Policy as DocumentParser
from sqlalchemy.exc import SQLAlchemyError
from app.models.db.db import db
from app.models.db.permission import Permission
from app.models.db.policy import Policy
from app.models.db.user import User


class UserUpdater:

    def __init__(self, iam_client, job_uuid):
        self.job_uuid = job_uuid
        self.iam = iam_client

    def _fill_user(self, user, aws_user, policies):
        user.name = aws_user['UserName']
        user.last_auth = aws_user.get('PasswordLastUsed') # This can be null
        user.arn = aws_user['Arn']
        user.foreign = False
        user.create_date = aws_user['CreateDate']
        user.updated_at = datetime.now()
        user.account = self.iam.get_account()
        user.job_uuid = self.job_uuid
        user.inline_count = aws_user['InlinePoliciesCount']
        for p in policies:
            user.policies.append(p)

    def _get_policies_from_aws_managed_policies(self,aws_managed_policies):
        managed_policies = []
        for aws_managed_policy in aws_managed_policies:
            policy = Policy.query.filter_by(arn=aws_managed_policy['PolicyArn']).first()
            if policy:
                managed_policies.append(policy)
            else:
                print(f"Could not get {aws_managed_policy}")
        return managed_policies


    def _get_policies_for_aws_user(self, aws_user_name):
        aws_managed_policies = self.iam.get_user_managed_policies(aws_user_name) # This doesn't include user managed policies inherit from groups
        return self._get_policies_from_aws_managed_policies(aws_managed_policies)

    def _get_users_from_aws_users(self, aws_users):
        for aws_user in aws_users:
            user = User.find_or_create(aws_user["Arn"])
            policies = self._get_policies_for_aws_user(aws_user['UserName'])
            self._fill_user(user, aws_user,policies)
            yield user

    def get_users(self):
        aws_users = self.iam.get_users()
        return self._get_users_from_aws_users(aws_users)

    def update_users(self):
        try:
            for user in self.get_users():
                db.session.add(user)
                db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error committing Users to the Database: \n {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()
