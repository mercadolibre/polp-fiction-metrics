from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from app.models.db.db import db

from app.models.db.role import Role
from app.models.db.permission import Permission
from app.models.db.policy import Policy
from app.models.db.service import Service
from app.models.db.account import Account
from app.models.db.user import User

from app.models.parsers.trust_relationship_parser import TrustRelationshipParser

class RoleUpdater:

    def __init__(self, iam_client, job_uuid):
        self.job_uuid = job_uuid
        self.iam = iam_client

    def _add_trusted_role(self, trust_policy, role):
        roles = trust_policy.get_trusted_principal_arns('role')
        role.trusted_roles.clear()
        for assuming_role in roles:
            trusted_role = Role.find_or_create(assuming_role.arn, foreign=True)
            if trusted_role.foreign:
                trusted_role.account = Account.find_or_create(assuming_role.account_number, foreign=True)
                trusted_role.job_uuid = self.job_uuid
            role.trusted_roles.append(trusted_role)
    
    def _add_trusted_users(self, trust_policy, role):
        users = trust_policy.get_trusted_principal_arns('user')
        role.trusted_users.clear()
        for user in users:
            trusted_user = User.find_or_create(user.arn, foreign=True)
            if trusted_user.foreign:
                trusted_user.account = Account.find_or_create(user.account_number, foreign=True)
                trusted_user.job_uuid = self.job_uuid
            role.trusted_users.append(trusted_user)

    def _add_trusted_services(self, trust_policy, role):
        services = trust_policy.get_trusted_services_names()
        role.trusted_services.clear()
        for srv in services:
            trusted_service = Service.find_or_create(srv)
            role.trusted_services.append(trusted_service)
    
    def _add_trusted_account(self, trust_policy, role):
        accounts = trust_policy.get_trusted_accounts_uuids()
        role.trusted_accounts.clear()      
        for acc in accounts:
            trusted_account = Account.find_or_create(acc, foreign=True)
            trusted_account.job_uuid = self.job_uuid
            role.trusted_accounts.append(trusted_account)

    def _add_trust_relationship(self, role, assume_policy_document):
        trust_policy = TrustRelationshipParser(assume_policy_document)
        self._add_trusted_account(trust_policy, role)
        self._add_trusted_services(trust_policy, role)
        self._add_trusted_users(trust_policy, role)
        self._add_trusted_role(trust_policy, role)
        self._set_external_entity_compliance(trust_policy, role)

    def _set_external_entity_compliance(self,trust_policy, role):
        compliance= trust_policy.is_compliant_for_external_entities()
        role.ext_entity_compliance = compliance

    def _fill_role(self, role, aws_role, policies):
        role.name = aws_role['RoleName']
        role.last_used = aws_role.get('RoleLastUsed')['LastUsedDate'] if aws_role.get('RoleLastUsed') else None
        role.last_used_regions = aws_role.get('RoleLastUsed')['Region'] if aws_role.get('RoleLastUsed') else None
        role.account = self.iam.get_account()
        role.job_uuid = self.job_uuid
        role.inline_count = aws_role['InlinePoliciesCount']
        role.foreign = False
        role.create_date = aws_role['CreateDate']
        for policy in policies:
            role.policies.append(policy)
        self._add_trust_relationship(role, aws_role['AssumeRolePolicyDocument'])


    def _get_policies_for_aws_managed_policies(self, managed_aws_policies):
        policies = []
        for managed_aws_policy in managed_aws_policies:
            policy = Policy.query.filter_by(arn=managed_aws_policy['PolicyArn']).first()
            if policy:
                policies.append(policy)
        return policies

    def _get_aws_policies_for_role(self, role_name):
        managed_aws_policies = self.iam.get_role_policies(role_name)
        return managed_aws_policies

    def _get_roles_from_aws_roles(self, aws_roles):
        for aws_role in aws_roles:
            role = Role.find_or_create(aws_role['Arn'])
            managed_aws_policies_for_role = self._get_aws_policies_for_role(aws_role['RoleName'])
            policies = self._get_policies_for_aws_managed_policies(managed_aws_policies_for_role)
            self._fill_role(role, aws_role, policies)
            yield role

    def get_roles(self):
        aws_roles = self.iam.get_roles() 
        return self._get_roles_from_aws_roles(aws_roles)

    def update_roles(self):
        try:
            for role in self.get_roles():
                db.session.add(role)
                db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error committing Policies to the Database: \n {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()
