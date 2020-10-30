from datetime import datetime

from policyuniverse.policy import Policy as DocumentParser
from sqlalchemy.exc import SQLAlchemyError
from app.models.db.db import db
from app.models.db.permission import Permission
from app.models.db.policy import Policy
from app.models.db.service import Service


class PolicyUpdater:

    def __init__(self, iam_client, job_uuid):
        self.job_uuid = job_uuid
        self.iam = iam_client

    def _fill_permission(self, permission, service_name, action):
        permission.service = Service.find_or_create(name=service_name)
        permission.reading = True if 'Read' in action else False
        permission.writing = True if 'Write' in action else False
        permission.listing = True if 'List' in action else False
        permission.tagging = True if 'Tagging' in action else False
        permission.managing = True if 'Permission' in action else False
        permission.job_uuid = self.job_uuid

    def _fill_policy(self, policy, aws_policy, permissions):
        policy.arn = aws_policy['Arn']
        policy.name = aws_policy['PolicyName']
        policy.update_date = aws_policy['UpdateDate']
        policy.attachment_count = aws_policy['AttachmentCount']
        policy.description = aws_policy.get('Description')
        policy.is_attachable = aws_policy['IsAttachable']
        policy.scope = aws_policy['Scope']
        policy.create_date = aws_policy['CreateDate']
        policy.account = self.iam.get_account()
        policy.job_uuid = self.job_uuid
        policy.updated_at = datetime.now()
        for p in permissions:
            policy.permissions.append(p)

    def _get_permission_from_summary(self, action_summary, policy):
        permissions = []
        for service_name, action in action_summary:
            new_permission = Permission()
            for p in policy.permissions:
                if p.service.name == service_name:
                    new_permission = p
                    break
            self._fill_permission(new_permission, service_name, action)
            permissions.append(new_permission)
        return permissions

    def _get_action_summary_from_aws_policy(self, aws_policy):
        policy_document = self.iam.get_policy_document(aws_policy['Arn'], aws_policy['DefaultVersionId'])
        action_summary = DocumentParser(policy_document).action_summary().items()
        return action_summary

    def _get_permissions_from_aws_policy(self, aws_policy, policy):
        action_summary = self._get_action_summary_from_aws_policy(aws_policy)
        return self._get_permission_from_summary(action_summary,policy)

    def _get_policies_from_response(self, aws_policies):
        for aws_policy in aws_policies:
            policy = Policy.find_or_create(aws_policy["Arn"], self.iam.get_account().id)
            permissions = self._get_permissions_from_aws_policy(aws_policy, policy)
            self._fill_policy(policy, aws_policy, permissions)
            yield policy

    def get_policies(self):
        aws_policies = self.iam.get_policies()
        return self._get_policies_from_response(aws_policies)

    def update_policies(self):
        try:
            for policy in self.get_policies():
                db.session.add(policy)
                db.session.commit()
        except SQLAlchemyError as e:
            print(f"Error committing Policies to the Database: \n {e}")
            db.session.rollback()
            raise
        finally:
            db.session.close()
