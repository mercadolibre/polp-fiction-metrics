from app.models.db.service import Service
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock


test_service_object = {
        "name": "s3"
        }

class TestAccount(TestCase):

    def setUp(self):
        self.service = Service(
                name = test_service_object['name'],
                )

    def test_constructor(self):
        print(self.service)
        assert self.service.name == test_service_object['name']


    @patch("app.models.db.service.Service")
    @patch("app.models.db.service.db")
    def test_find_or_create(self, mock_db,mock_service):
        service = Service(name="s3")
        mock_service.query.filter_by.return_value.first.return_value = "string"
        service = Service.find_or_create("s3")
        assert service == "string"


    @patch("app.models.db.service.Service.query")
    @patch("app.models.db.service.db")
    def test_find_or_create(self, mock_db,mock_service):
        mock_service.filter_by.return_value.first.return_value = None
        service_new = Service(name="s3")
        service = Service.find_or_create("s3")
        assert service.name == service_new.name

