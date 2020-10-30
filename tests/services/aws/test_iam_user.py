from unittest import mock, TestCase
from app.models.db.account import Account
from app.services.aws.iam import IAM
from datetime import datetime



aws_users = {
		'Users': [
			{
				'Path': 'string',
				'UserName': 'string',
				'UserId': 'string',
				'Arn': 'string',
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
				},
			],
		'IsTruncated': False,
		'Marker': 'string'
		}

aws_users2 = {
		'Users': [
			{
				'Path': 'string',
				'UserName': 'string',
				'UserId': 'string',
				'Arn': 'string',
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
				},
			],
		'IsTruncated': False,
		'Marker': 'string'
		}

list_user_policies_response = {
    'PolicyNames': [
        'string'
        ],
    'IsTruncated': False,
    'Marker': 'string'
    }

class TestIAMUsers(TestCase):

    def setUp(self):
    	self.acc = Account(name="account",uuid="123456789")

	# def test_get_account(self):
		# iam = IAM(self.acc)
		# assert iam.get_account() == self.acc

    def test_get_policies(self):
        with mock.patch('app.services.aws.iam.AssumeRole') as mocked_assume_role:
            mocked_assume_role.return_value.get_client.return_value.list_users.side_effect = [aws_users,aws_users2]
            mocked_assume_role.return_value.get_client.return_value.list_user_policies.return_value = list_user_policies_response
            iam = IAM(self.acc)
			# iam.client.list_policies.return_value = aws_policies                       
            users = iam.get_users()
            print(users)
			# assert policies[0]['Scope'] == "AWS" 
			# assert policies[1]['Scope'] == "Local" 


