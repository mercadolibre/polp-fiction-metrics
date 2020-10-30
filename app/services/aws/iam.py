from app.config import POLP_FICTION_ROLE
from app.services.aws.assume_role import AssumeRole
from app.services.aws.iam_identities.policies import IAMPolicies
from app.services.aws.iam_identities.access_advisor import AccessAdvisor
from app.services.aws.iam_identities.roles import IAMRoles
from app.services.aws.iam_identities.users import IAMUsers


class IAM():

    def __init__(self, account):
        session = AssumeRole(account.uuid, POLP_FICTION_ROLE)
        self.account = account
        self.client = session.get_client('iam')
        self.users = IAMUsers(self.client)
        self.roles = IAMRoles(self.client)
        self.policies = IAMPolicies(self.client)
        self.access_advisor = AccessAdvisor(self.client)
        print(f"Iam initialized for {self.account}")

    def get_account(self):
        return self.account

    def get_last_access_data_for_arns(self, arns):
        return self.access_advisor.get_last_access_data(arns)

    # Policy methods
    def get_policy_document(self, arn, version_id):
        return self.policies.get_policy_document(arn, version_id)

    def get_policies(self):
        return self.policies.get_policies()

    # Role methods
    def get_roles(self):
        return self.roles.get_roles()

    def get_role_policies(self, role_name):
        return self.roles.get_role_policies(role_name)

    # User methods
    def get_user_managed_policies(self, user_name):
        return self.users.get_user_managed_policies(user_name)

    def get_users(self):
        return self.users.get_users()
