from app.models.db.account import Account
from app.models.db.role import Role
from app.models.db.policy import Policy
from app.models.db.user import User 
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch


test_account_object = {
        "uuid" : "1234567890",
        "foreign": True,
        "name": "cloudsec",
        "created_at": datetime.now(),
        }

class TestAccount(TestCase):

    def setUp(self):
        self.account = Account(
                uuid = test_account_object['uuid'],
                foreign = test_account_object['foreign'],
                name = test_account_object['name'],
                created_at = test_account_object['created_at']
                )


    def test_acc_constructor(self):
        assert self.account.uuid == test_account_object['uuid']
        assert self.account.foreign == test_account_object['foreign']
        assert self.account.name == test_account_object['name']
        assert self.account.created_at == test_account_object['created_at']
        print(self.account)
        assert self.account.updated_at == None

    def test_add_to_account(self):
        role_1 = Role(
                name="role_1",
                arn="arn_role_1"
                )
        role_2 = Role(
                name="role_2",
                arn="arn_role_2"
                )
        print(role_2)
        self.account.roles.append(role_1)
        assert len(self.account.roles) == 1
        assert self.account.roles[0] == role_1
        self.account.roles.append(role_2)
        assert len(self.account.roles) == 2


    def test_add_u_to_account(self):
        user_1 =User(
                name="1",
                arn="arn_1"
                )
        user_2 = User(
                name="2",
                arn="arn_2"
                )
        print(user_2)
        self.account.users.append(user_1)
        assert self.account.users[0] == user_1
        assert len(self.account.users) == 1
        self.account.users.append(user_2)
        assert len(self.account.users) == 2
    
    def test_add_policy_to_account(self):
        policy_1 = Policy(
                name="1",
                arn="arn_1"
                )
        policy_2 = Policy(
                name="2",
                arn="arn_2"
                )
        print(policy_2)
        self.account.policies.append(policy_1)
        assert self.account.policies[0] == policy_1
        assert len(self.account.policies) == 1
        self.account.policies.append(policy_2)
        assert len(self.account.policies) == 2

    @patch('app.models.db.user.db.session.query')
    def test_find_or_create(self, mock_db_query):
        account_new = Role(arn='arn')
        mock_db_query.return_value.filter_by.return_value.first.return_value = account_new
        account = Account.find_or_create("arn")
        assert account.arn == account_new.arn
        assert account == account_new