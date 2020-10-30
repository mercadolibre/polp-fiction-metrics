from app.models.db.account import Account
from app.models.db.role import Role
from app.models.db.policy import Policy
from app.models.db.user import User 
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch



test_user_object= {
        "name" : "name",
        "arn": "arn",
        "job_uuid": "cloudsec",
        "created_at": datetime.now(),
        }

class TestUser(TestCase):

    def setUp(self):
        self.user= User(
                arn= test_user_object['arn'],
                job_uuid = test_user_object['job_uuid'],
                created_at = test_user_object['created_at'],
                name = test_user_object['name'],
                )

    def test_constructor(self):
        print(self.user)
        assert self.user.name == test_user_object['name']

    @patch('app.models.db.user.db.session.query')
    def test_find_or_create(self, mock_db_query):
        user_new = User(arn='arn')
        mock_db_query.return_value.filter_by.return_value.first.return_value = user_new
        user = User.find_or_create("arn")
        assert user.arn == user_new.arn
        assert user == user_new


