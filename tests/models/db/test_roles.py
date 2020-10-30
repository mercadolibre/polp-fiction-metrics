from app.models.db.role import Role
from app.models.db.policy import Policy
from app.models.db.account import Account
from app.models.db.service import Service
from app.models.db.user import User 
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch


test_role_object = {
        "arn" : "test_arn",
        "name": "",
        "last_used" : datetime.now(),
        "created_at": datetime.now(),
        }

class Testrole(TestCase):

    def setUp(self):
        self.role = Role(
                arn=test_role_object['arn'],
                name = test_role_object['name'],
                last_used = test_role_object['last_used'],
                created_at = test_role_object['created_at']
                )

    def test_constructor(self):
        assert self.role.arn== test_role_object['arn']
        assert self.role.last_used== test_role_object['last_used']
        assert self.role.name == test_role_object['name']
        assert self.role.created_at == test_role_object['created_at']
        assert self.role.updated_at == None

    def set_account_to_role(self):
        acc = Account(
                uuid =  "123456789",
                provider =  "AWS",
                name =  "test_account",
                created_at = datetime.now()
                )

        self.role.account = acc
        assert self.role.account == acc
        assert self.role.account.name == "123456789"

    def test_add_policy_to_role(self):
        policy_1 = Policy(
                name="1",
                arn="arn_1"
                )
        policy_2 = Policy(
                name="2",
                arn="arn_2"
                )
        self.role.policies.append(policy_1)
        assert self.role.policies[0] == policy_1
        assert len(self.role.policies) == 1
        self.role.policies.append(policy_2)
        assert len(self.role.policies) == 2
    
    def test_trusted_user(self):
        role = Role(
                arn=test_role_object['arn'],
                name = test_role_object['name'],
                last_used = test_role_object['last_used'],
                created_at = test_role_object['created_at']
                )
        user = User(
                name="trusted_user",
                arn="arn_trusted"
                )
        user2 = User(
                name="trusted_user2",
                arn="arn_trusted2"
                )
        role.trusted_users.append(user)
        role.trusted_users.append(user2)
        assert role.trusted_users[0] == user
        assert role.trusted_users[1] == user2

    def test_trusted_account(self):
        role = Role(
                arn=test_role_object['arn'],
                name = test_role_object['name'],
                last_used = test_role_object['last_used'],
                created_at = test_role_object['created_at']
        )
        acc = Account(uuid="123123123", name="Namef")
        role.trusted_accounts.append(acc)
        assert role.trusted_accounts[0].name == "Namef"

    def test_trusted_role(self):
        role = Role(
                arn=test_role_object['arn'],
                name = test_role_object['name'],
                last_used = test_role_object['last_used'],
                created_at = test_role_object['created_at']
        )
        assuming_role = Role(arn="arn", name="Namef")
        role.trusted_roles.append(assuming_role)
        assert role.trusted_roles[0].arn == "arn"
    
    def test_trusted_services(self):
        role = Role(
                arn=test_role_object['arn'],
                name = test_role_object['name'],
                last_used = test_role_object['last_used'],
                created_at = test_role_object['created_at']
        )
        service = Service(name="s3")
        role.trusted_services.append(service)
        assert role.trusted_services[0].name == "s3"

    def test_trusted_role(self):
        role = Role(
                arn=test_role_object['arn'],
                name = test_role_object['name'],
                last_used = test_role_object['last_used'],
                created_at = test_role_object['created_at']
        )
        trusted_role = Role(arn="arn", name="Namef")
        role.trusted_roles.append(trusted_role)
        assert role.trusted_roles[0].arn == "arn"
        
    @patch('app.models.db.user.db.session.query')
    def test_find_or_create(self, mock_db_query):
        role_new = Role(arn='arn')
        mock_db_query.return_value.filter_by.return_value.first.return_value = role_new
        role = Role.find_or_create("arn")
        assert role.arn == role_new.arn
        assert role == role_new
