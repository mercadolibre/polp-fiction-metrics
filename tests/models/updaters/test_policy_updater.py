from unittest import mock, TestCase
from sqlalchemy.exc import SQLAlchemyError
import os
from app.models.updaters.policy_updater import PolicyUpdater
from app.models.db.policy import Policy, Permission
from app.models.db.service import Service

class PolicyUpdaterTestCase(TestCase):

    def setUp(self):
        job_uuid = 'hoy_es_hoy' 
        iam_client = mock.MagicMock()
        iam_client.get_policies.return_value = [{
            'PolicyName': 'string',
            'PolicyId': 'string',
            'Arn': 'string',
            'Path': 'string',
            'DefaultVersionId': 'string',
            'AttachmentCount': 123,
            'PermissionsBoundaryUsageCount': 123,
            'IsAttachable': True,
            'Description': 'string',
            'CreateDate': '2015-01-01',
            'UpdateDate': '2015-01-01',
            'Scope': 'test'
        }]
        self.policy_updater = PolicyUpdater(iam_client, job_uuid)


    def test_get_account_polcies(self):
        # mock.patch('app.models.updaters.policy_updater.Permission') as mocked_Permission,\
        with mock.patch('app.models.updaters.policy_updater.db') as mocked_db,\
            mock.patch('app.models.updaters.policy_updater.Policy') as mocked_Policy:

            try:
                response = self.policy_updater.update_policies()
            except Exception as e:
                self.fail(f'test_get_account fail with error: {e}!')

    def test_get_accounts_failure(self):
        # mock.patch('app.models.updaters.policy_updater.Permission') as mocked_Permission,\
        with mock.patch('app.models.updaters.policy_updater.db') as mocked_db,\
            mock.patch('app.models.updaters.policy_updater.Policy') as mocked_Policy:
            mocked_db.session.add.side_effect = SQLAlchemyError

            self.assertRaises(SQLAlchemyError, self.policy_updater.update_policies)

#    def test_permission_filler(self):
#        with mock.patch('app.models.updaters.policy_updater.db') as mocked_db,\
#            mock.patch('app.models.db.permission.db') as mocked_permission_db,\
#            mock.patch('app.models.db.policy.db') as mocked_policy_db,\
#            mock.patch('app.models.db.service.db') as mocked_service_db:
#            # mock.patch('app.models.updaters.policy_updater.Policy') as mocked_Policy\
#            # mock.patch('app.models.updaters.policy_updater.Permission') as mocked_Permission\
#            action_summary = [('s3',['Read'])]
#            p1 = Policy(arn='arn:1')
#            pe1 = Permission()
#            pe2 = Permission()
#            pe1.service = Service(name='sqs')
#            pe2.service = Service(name='s3')
#            p1.permissions.append(pe1)
#            p1.permissions.append(pe2)
#            policy_updater = PolicyUpdater('iam_client', 'job_uuid')
#            permissions = policy_updater._get_permission_from_summary(action_summary, p1)
