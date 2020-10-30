from unittest import mock, TestCase
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import os
from app.models.updaters.user_updater import UserUpdater


class UserUpdaterTestCase(TestCase):

    def setUp(self):
        job_uuid = 'hoy_es_hoy' 
        iam_client = mock.MagicMock()
        iam_client.get_users.return_value = [{
            'Path': 'string',
            'UserName': 'string',
            'UserId': 'string',
            'Arn': 'string',
            'InlinePoliciesCount': 'string',
            'CreateDate': datetime(2015, 1, 1),
            'PasswordLastUsed': datetime(2015, 1, 1),
            'PermissionsBoundary': {
                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                'PermissionsBoundaryArn': 'string'
            },
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        }
        ]
        self.user_updater = UserUpdater(iam_client, job_uuid)


    def test_update_users(self):
        with mock.patch('app.models.updaters.user_updater.db') as mocked_db,\
            mock.patch('app.models.updaters.user_updater.Policy') as mocked_Policy,\
            mock.patch('app.models.updaters.user_updater.User') as mocked_User:
            try:
                response = self.user_updater.update_users()
            except Exception as e:
                self.fail(f'test_update_users fail with error: {e}!')

    def test_update_users_fail(self):

        with mock.patch('app.models.updaters.user_updater.db') as mocked_db,\
            mock.patch('app.models.updaters.user_updater.Policy') as mocked_Policy,\
            mock.patch('app.models.updaters.user_updater.User') as mocked_User:

            mocked_db.session.add.side_effect = SQLAlchemyError

            self.assertRaises(SQLAlchemyError, self.user_updater.update_users)
