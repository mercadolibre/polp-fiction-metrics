from unittest import mock, TestCase
from app.models.db.account import Account
from app.services.aws.iam import IAM
from datetime import datetime



aws_policies = {'Policies': [
		{
			'PolicyName': 'string',
			'PolicyId': 'string',
			'Arn': 'string',
			'Path': 'string',
			'DefaultVersionId': 'string',
			'AttachmentCount': 123,
			'PermissionsBoundaryUsageCount': 123,
			'IsAttachable': True,
			'Description': 'string',
			'CreateDate': datetime(2015, 1, 1),
			'UpdateDate': datetime(2015, 1, 1)
			},
		],
		'IsTruncated': False,
		'Marker': 'string'
		}
aws_policies2 = {'Policies': [
		{
			'PolicyName': 'string',
			'PolicyId': 'string',
			'Arn': 'string',
			'Path': 'string',
			'DefaultVersionId': 'string',
			'AttachmentCount': 123,
			'PermissionsBoundaryUsageCount': 123,
			'IsAttachable': True,
			'Description': 'string',
			'CreateDate': datetime(2015, 1, 1),
			'UpdateDate': datetime(2015, 1, 1)
			},
		],
		'IsTruncated': False,
		'Marker': 'string'
		}

class TestIAM(TestCase):

    def setUp(self):
        self.acc = Account(name="account",uuid="123456789") 
    # Mockear IAM
    # def test_get_account(self):
        # iam = IAM(self.acc)
        # assert iam.get_account() == self.acc

    def test_get_policies(self):
        with mock.patch('app.services.aws.iam.AssumeRole') as mocked_assume_role:
            mocked_assume_role.return_value.get_client.return_value.list_policies.side_effect = [aws_policies,aws_policies2]
            iam = IAM(self.acc)
            policies = iam.get_policies()
            assert policies[0]['Scope'] == "AWS" 
            assert policies[1]['Scope'] == "Local"

    def test_get_policy_document(self):
        with mock.patch('app.services.aws.iam.AssumeRole') as mocked_assume_role:
            mock_response = {
                    "PolicyVersion": {
                    "Document": {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": [
                                    "iq:*",
                                    "iq-permission:*"
                                ],
                                "Effect": "Allow",
                                "Resource": "*"
                            },
                            {
                                "Effect": "Allow",
                                "Action": "iam:CreateServiceLinkedRole",
                                "Resource": "*",
                                "Condition": {
                                    "StringEquals": {
                                        "iam:AWSServiceName": [
                                            "permission.iq.amazonaws.com",
                                            "contract.iq.amazonaws.com"
                                        ]
                                    }
                                }
                            }
                        ]
                    },
                    "VersionId": "v2",
                    "CreateDate": "2019-09-25T20:22:34Z"
                }
                }
            mocked_assume_role.return_value.get_client.return_value.get_policy_version.return_value = mock_response
            iam = IAM(self.acc)
            response = iam.get_policy_document('arn', 'v2')
            print(response)
            self.assertEqual(response['Statement'][0]['Resource'], '*')


    def test_get_roles(self):
        with mock.patch('app.services.aws.iam.AssumeRole') as mocked_assume_role:
            mock_response = {
                "Roles": [
                    {
                        "Path": "/",
                        "RoleName": "AccountsManagementRole",
                        "RoleId": "AROAI7C5BIHEEEEEEEE",
                        "Arn": "arn:aws:iam::696969696972:role/Role1",
                        "CreateDate": "2018-08-22T20:35:03Z",
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
                    },
                    {
                        "Path": "/",
                        "RoleName": "admin_queue",
                        "RoleId": "AROAI7C5BIHEEEEEEEH",
                        "Arn": "arn:aws:iam::696969696969:role/admin_queue",
                        "CreateDate": "2018-11-22T18:24:46Z",
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {
                                        "Service": "ec2.amazonaws.com"
                                    },
                                    "Action": "sts:AssumeRole"
                                }
                            ]
                        },
                        "MaxSessionDuration": 3600
                    },
                    ],
                    'IsTruncated': False,
		            'Marker': 'string'
                    }
            mocked_list_role_policies = {
                'PolicyNames': [
                    'string',
                    ],
                    'IsTruncated': False,
                    'Marker': 'string'
                    }

            mocked_assume_role.return_value.get_client.return_value.list_roles.return_value = mock_response
            mocked_assume_role.return_value.get_client.return_value.list_role_policies.return_value = mocked_list_role_policies
            iam = IAM(self.acc)
            response = iam.get_roles()
            self.assertEqual(response[0]['RoleId'], 'AROAI7C5BIHEEEEEEEE')
    
    def test_get_role_policies(self):
        with mock.patch('app.services.aws.iam.AssumeRole') as mocked_assume_role:
            mock_response = {
                'AttachedPolicies': [
                    {
                        'PolicyName': 'La policy del role: tu_role',
                        'PolicyArn': 'string'
                    },
                ],
                'IsTruncated': False,
                'Marker': 'string'
            }
            mocked_assume_role.return_value.get_client.return_value.\
                list_attached_role_policies.return_value = mock_response
            iam = IAM(self.acc)
            response = iam.get_role_policies('tu_role')
            self.assertEqual(response[0]['PolicyName'], 'La policy del role: tu_role')      

    def test_get_user_policies(self):
        with mock.patch('app.services.aws.iam.AssumeRole') as mocked_assume_role:
            mock_response = {
                'AttachedPolicies': [
                    {
                        'PolicyName': 'La policy del role: tu_role',
                        'PolicyArn': 'string'
                    },
                ],
                'IsTruncated': False,
                'Marker': 'string'
            }
            mocked_assume_role.return_value.get_client.return_value.\
                list_attached_user_policies.return_value = mock_response
            iam = IAM(self.acc)
            response = iam.get_user_managed_policies('tu_role')
            self.assertEqual(response[0]['PolicyName'], 'La policy del role: tu_role')      
