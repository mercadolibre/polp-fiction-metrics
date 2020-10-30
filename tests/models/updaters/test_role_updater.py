from unittest import mock, TestCase
from sqlalchemy.exc import SQLAlchemyError
from app.models.updaters.role_updater import RoleUpdater


class RoleUpdaterTestCase(TestCase):

    def setUp(self):
        job_uuid = 'hoy_es_hoy' 
        iam_client = mock.MagicMock()
        iam_client.get_roles.return_value = [
            {
                "Path": "/",
                "RoleName": "AccountsManagementRole",
                "RoleId": "AROAI7C5BIHEEEEEEEE",
                "Arn": "arn:aws:iam::696969696972:role/Role1",
                "CreateDate": "2018-08-22T20:35:03Z",
                "InlinePoliciesCount": "2018-08-22T20:35:03Z",
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": "arn:aws:iam::696969696969:role/AssumeInstanceRoleTA",
                                "Service": "ec2.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                },
                "MaxSessionDuration": 3600
            }
        ]

        iam_client.get_role_policies.return_value = [
            {
                'PolicyName': 'La policy del role: tu_role',
                'PolicyArn': 'string'
            }
        ]

        self.role_updater = RoleUpdater(iam_client, job_uuid)


    def test_update_roles(self):
        with mock.patch('app.models.updaters.role_updater.db') as mocked_db,\
            mock.patch('app.models.updaters.role_updater.Policy') as mocked_policy,\
            mock.patch('app.models.updaters.role_updater.User') as mocked_policy,\
            mock.patch('app.models.updaters.role_updater.Service') as mocked_policy,\
            mock.patch('app.models.updaters.role_updater.Account') as mocked_policy,\
            mock.patch('app.models.updaters.role_updater.Role') as mocked_role:

            try:
                response = self.role_updater.update_roles()
            except Exception as e:
                self.fail(f'test_update_roles fail with error: {e}!')

    def test_update_roles_fail(self):

        with mock.patch('app.models.updaters.role_updater.db') as mocked_db,\
            mock.patch('app.models.updaters.role_updater.Policy') as mocked_policy,\
            mock.patch('app.models.updaters.role_updater.Role') as mocked_role:

            mocked_db.session.add.side_effect = SQLAlchemyError

            self.assertRaises(SQLAlchemyError, self.role_updater.update_roles)

