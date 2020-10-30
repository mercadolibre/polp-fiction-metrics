class IAMUsers():

    def __init__(self, iam):
        self.client = iam

    # User methods
    def _users_marker_handler(self, marker=None):
        if marker:
            response = self.client.list_users(Marker=marker)
        else:
            response = self.client.list_users()
        return response

    def _attached_policies_marker_handler(self, user_name, marker=None):
        if marker:
            response = self.client.list_attached_user_policies(Marker=marker, UserName=user_name)
        else:
            response = self.client.list_attached_user_policies(UserName=user_name)
        return response

    def get_user_managed_policies(self, user_name):
        att_policies = []
        marker = None
        while True:
            resp = self._attached_policies_marker_handler(user_name, marker)
            for att_policy in resp['AttachedPolicies']:
                att_policies.append(att_policy)
            marker = resp.get('Marker')
            if not resp['IsTruncated']:
                break
        return att_policies

    def _inline_policies_marker_handler(self, username, marker=None):
        if marker:
            response = self.client.list_user_policies(Marker=marker, UserName=username)
        else:
            response = self.client.list_user_policies(UserName=username)
        return response
    
    def _get_user_inline_policies_count(self, username):
        marker = None
        inline_policies_count = 0
        while True:
            resp = self._inline_policies_marker_handler(username, marker)
            inline_policies_count += len(resp['PolicyNames'])
            marker = resp.get('Marker')
            if not resp['IsTruncated']:
                break
        return inline_policies_count

    def get_users(self):
        users = []
        marker = None
        while True:
            resp = self._users_marker_handler(marker)
            for user in resp['Users']:
                user['InlinePoliciesCount'] = self._get_user_inline_policies_count(user['UserName'])
                users.append(user)
            marker = resp.get('Marker')
            if not resp['IsTruncated']:
                break
        return users
