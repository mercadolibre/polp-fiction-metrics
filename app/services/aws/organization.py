from app.services.aws.assume_role import AssumeRole
from app.config import BLACK_LIST, POLP_FICTION_ORGANIZATIONS_ROLE, POLP_FICTION_MASTER_ACCOUNT
class Organization():


    def __init__(self):
        # Initialize client
        master_account =  POLP_FICTION_MASTER_ACCOUNT
        master_role = POLP_FICTION_ORGANIZATIONS_ROLE
        session = AssumeRole(master_account, master_role)
        self.client = session.get_client('organizations')

    def _token_handler(self, next_token=None):
        if next_token:
            response = self.client.list_accounts(
                NextToken = next_token
            )
        else:
            response = self.client.list_accounts()

        return response
    
    def get_accounts(self):
        # Get all accounts data from AWS organizations and give it back to the controller.
        accounts = {}

        done = False
        token = None
        try:
            while done == False:
                resp = self._token_handler(token)
                for account in resp['Accounts']:
                    if account['Status'] == 'ACTIVE' and account['Id'] not in BLACK_LIST:
                        accounts[account['Id']] = account['Name']
                if 'NextToken' in resp:
                    token = resp['NextToken']
                else:
                    done = True
        except Exception:
            raise

        return accounts

