from unittest import TestCase, mock
from policyuniverse.arn import ARN
from app.models.parsers.trust_relationship_parser import TrustRelationshipParser

document = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::123456789013:root",
          "arn:aws:iam::234556789321:user/usrtl123",
          "AIDAIGBHOGBB77AOZ4LE2",
          "arn:aws:iam::888222333221:role/AssumeInstanceRoleTA"
        ],
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::234556789321:user/usermgr123",
        "Service": [
          "ec2.amazonaws.com",
          "s3.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}

document_external_id = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::123456789013:root",
          "arn:aws:iam::234556789321:user/usrtl123",
          "AAAAAAAAAAAAAAAAAAAAAA",
          "arn:aws:iam::888222333221:role/AssumeInstanceRoleTA"
        ],
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {"StringEquals": {"sts:ExternalId": "Unique ID Assigned by Example Corp"}}
    }
  ]
}

class TrustRelationshipParserTestCase(TestCase):

    def setUp(self):
        self.trust_parser = TrustRelationshipParser(document)
        self.trust_parser_ext_id = TrustRelationshipParser(document_external_id)
    
    def test_get_principal_users(self):
        users = self.trust_parser.get_trusted_principal_arns('user')
        self.assertIn('user/usrtl123', list(map(lambda u: u.name, users)))
        self.assertIn('user/usermgr123', list(map(lambda u: u.name, users)))

    def test_get_principal_account(self):
        # self.assertEqual("arn:aws:iam::123456789013:root",)
        self.assertEqual(self.trust_parser.get_trusted_principal_arns('root')[0].arn,ARN('arn:aws:iam::123456789013:root').arn)


    def test_get_principal_role(self):
        self.assertEqual(self.trust_parser.get_trusted_principal_arns('role')[0].arn,ARN('arn:aws:iam::888222333221:role/AssumeInstanceRoleTA').arn)

    def test_get_principal_services(self):
        services = self.trust_parser.get_trusted_services_names()
        self.assertIn('ec2', services)
        self.assertIn('s3', services)
        self.assertIn('lambda', services)

    def test_get_principal_account_uuids(self):
        self.assertEqual(
            self.trust_parser.get_trusted_accounts_uuids(),
            ['123456789013'])

    def test_external_entity_not_compliant(self):
        self.assertEqual(
            self.trust_parser.is_compliant_for_external_entities(),
            False)

    def test_external_entity_compliant(self):
        self.assertEqual(
            self.trust_parser_ext_id.is_compliant_for_external_entities(),
            True)


    
