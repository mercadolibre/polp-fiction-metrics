from unittest import mock, TestCase
from sqlalchemy.exc import SQLAlchemyError
import os
from app.models.updaters.access_updater import AccessUpdater
from app.models.db.permission import Permission
from app.models.db.service import Service
from app.models.db.policy import Policy
from unittest.mock import patch, MagicMock



class AccessUpdaterTestCase(TestCase):

    # def setUp(self):
        # job_uuid = 'hoy_es_hoy' 
        # iam_client = mock.MagicMock()
        # iam_client.get_policies.return_value = [{
            # 'PolicyName': 'string',
            # 'PolicyId': 'string',
            # 'Arn': 'string',
            # 'Path': 'string',
            # 'DefaultVersionId': 'string',
            # 'AttachmentCount': 123,
            # 'PermissionsBoundaryUsageCount': 123,
            # 'IsAttachable': True,
            # 'Description': 'string',
            # 'CreateDate': '2015-01-01',
            # 'UpdateDate': '2015-01-01',
            # 'Scope': 'test'
        # }]
        # self.policy_updater = PolicyUpdater(iam_client, job_uuid)

    @patch('app.models.updaters.access_updater.Policy')
    def test_get_policies(self,policy_mock):
        iam = MagicMock()
        au = AccessUpdater(iam,"account_id")
        policy_mock.query.filter_by.return_value.all.return_value = [1,2,3]
        assert au._get_policies() == [1,2,3]

    @patch('app.models.updaters.access_updater.Policy')
    @patch('app.models.updaters.access_updater.db')
    def test_update_last_access_policies(self,db_mock,policy_mock):
        iam = MagicMock()
        iam.get_last_access_data_for_arn.return_value = {'arn:1':{'LasAuthenticated'}}
        au = AccessUpdater(iam,"account_id")
        p1 = Policy(arn='arn:1')
        p2 = Policy(arn='arn:2')
        pe1 = Permission()
        pe2 = Permission()
        pe1.service = Service(name='sqs')
        pe2.service = Service(name='s3')
        permissions = [pe1,pe1]
        p1.permissions.append(pe1)
        p2.permissions.append(pe2)
        policy_mock.query.filter_by.return_value.all.return_value = [p1,p2]
        au.update_policies_last_access()
        assert au._get_policies() == [p1,p2]
        assert pe1==pe1

    @patch('app.models.updaters.access_updater.Policy')
    @patch('app.models.updaters.access_updater.db')
    def test_update_last_access_policies_exception(self,db_mock,policy_mock):
        db_mock.session.add.side_effect = SQLAlchemyError
        iam = MagicMock()
        iam.get_last_access_data_for_arn.return_value = {'arn:1':{'LasAuthenticated'}}
        au = AccessUpdater(iam,"account_id")
        p1 = Policy(arn='arn:1')
        p2 = Policy(arn='arn:2')
        pe1 = Permission()
        pe2 = Permission()
        pe1.service = Service(name='sqs')
        pe2.service = Service(name='s3')
        permissions = [pe1,pe1]
        p1.permissions.append(pe1)
        p2.permissions.append(pe2)
        policy_mock.query.filter_by.return_value.all.return_value = [p1,p2]
        try:
            au.update_policies_last_access()
            assert False
        except SQLAlchemyError:
            assert True
