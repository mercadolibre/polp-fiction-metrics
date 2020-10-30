from unittest import mock, TestCase
import os
from app.services.aws.organization import Organization

# os.environ['SCOPE'] = "DEV"

class OrganizationTestCase(TestCase):


    def test_get_accounts(self):

        with mock.patch('app.services.aws.organization.AssumeRole') as mocked_assume_role:    
            mocked_assume_role.return_value.get_client.return_value.\
                list_accounts.return_value = {'Accounts':[{'Id': '121212121212',
                'Arn': 'arn:aws:organizations::191919191919:account/o-mengueche/121212121212',
                'Email': 'aws.ble@ble.com',
                'Name': 'ble-account',
                'Status': 'ACTIVE',
                'JoinedMethod': 'INVITED',
                'JoinedTimestamp': 1585580413.66},
                {'Id': '696969696969',
                'Arn': 'arn:aws:organizations::191919191919:account/o-mengueche/696969696969',
                'Email': 'awsaccounts+ble2@ble.com',
                'Name': 'ble2-account',
                'Status': 'ACTIVE',
                'JoinedMethod': 'CREATED',
                'JoinedTimestamp': 1585580413.66}]
            }

            org_client = Organization()
            response = org_client.get_accounts()
            self.assertEqual(response, {'121212121212' :'ble-account', '696969696969' : 'ble2-account'})
    
    def test_token_handler(self):

        with mock.patch('app.services.aws.organization.AssumeRole') as mocked_assume_role:
            
            org_client = Organization()
            org_client._token_handler(next_token='el_token')
            mocked_assume_role.return_value.get_client.return_value.\
                list_accounts.assert_called_with(NextToken='el_token')


    def test_get_accounts_fail(self):

        with mock.patch('app.services.aws.organization.Organization._token_handler') as mocked_token_handler:
            
            mocked_token_handler.side_effect = Exception()
            try:
                org_client = Organization()
                assert False
            except Exception:
                assert True
            # self.assertRaises(Exception, org_client.get_accounts, ())
