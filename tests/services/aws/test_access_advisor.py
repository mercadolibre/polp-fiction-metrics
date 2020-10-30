from app.services.aws.iam_identities.access_advisor import AccessAdvisor

from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch

class AccessAdvisorTestCase(TestCase):
    
    def setUp(self):
        iam = MagicMock()
        iam.generate_service_last_accessed_details.side_effect = [{'JobId': 'Que detalle'}, Exception()]
        iam.get_service_last_accessed_details.side_effect = [
            {'JobStatus': 'COMPLETED',
            'ServicesLastAccessed': [
                {'ServiceNamespace': 'string'}
                ]
            },
            {'JobStatus': 'IN_PROGRESS',
            'ServicesLastAccessed': [
                {'ServiceNamespace': 'string'}
                ]
            }
        ]
        self.access_advisor = AccessAdvisor(iam)

    def test_generate_service_last_accessed_details(self):
         self.assertEqual(self.access_advisor._generate_service_last_accessed_details('arn'), 'Que detalle')

    def test_generate_service_last_accessed_details_fail(self):
        try:
            self.access_advisor._generate_service_last_accessed_details('arn')
            assert False
        except Exception:
            assert True

    def test_get_last_access_data(self):
        self.assertEqual({'arn1': {'string': {}}}, self.access_advisor.get_last_access_data(['arn1', 'arn2']))
        self.assertEqual({}, self.access_advisor.get_last_access_data(['arn1', 'arn2']))

        
