class IAMRoles():

    def __init__(self, iam):
        self.client = iam

    # Role methods
    def _role_marker_handler(self, marker=None):
        if marker:
            response = self.client.list_roles(
                    Marker=marker
                    )
        else:
            response = self.client.list_roles()
        return response

    def _get_roles_marker_handler(self):
        roles = []
        marker = None
        while True:
            resp = self._role_marker_handler(marker)
            for role in resp['Roles']:
                roles.append(role)
            marker = resp.get('Marker')
            if not resp['IsTruncated']:
                break
        return roles

    def get_roles(self, last_access=True):
        roles = self._get_roles_marker_handler()
        if last_access:
            for role in roles:
                role['RoleLastUsed'] = self._get_role_last_used(role['RoleName'])
                role['InlinePoliciesCount'] = self._get_role_inline_policies_count(role['RoleName'])
        return roles

    def _get_role_last_used(self,role_name):
        return self.client.get_role(RoleName=role_name)['Role'].get('RoleLastUsed')

    def _role_policies_marker_handler(self, role_name, marker=None):
        if marker:
            response = self.client.list_attached_role_policies(
                    RoleName=role_name,
                    Marker=marker
                    )
        else:
            response = self.client.list_attached_role_policies(
                    RoleName=role_name
                    )
        return response

    def _role_inline_policies_marker_handler(self, role_name, marker=None):
        if marker:
            response = self.client.list_role_policies(
                    RoleName=role_name,
                    Marker=marker
                    )
        else:
            response = self.client.list_role_policies(
                    RoleName=role_name
                    )
        return response

    def _get_role_inline_policies_count(self, role_name):
        marker = None
        inline_policies_count = 0
        while True:
            resp = self._role_inline_policies_marker_handler(role_name, marker)
            inline_policies_count += len(resp["PolicyNames"])
            marker = resp.get('Marker')
            if not resp['IsTruncated']:
                break
        return inline_policies_count

    def get_role_policies(self, role_name):
        policies = []
        marker = None
        while True:
            resp = self._role_policies_marker_handler(role_name, marker)
            for policy in resp['AttachedPolicies']:
                policies.append(policy)
            marker = resp.get('Marker')
            if not resp['IsTruncated']:
                break
        return policies
