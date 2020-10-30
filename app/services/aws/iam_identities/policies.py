class IAMPolicies():

    def __init__(self, iam):
        self.client = iam

    def _marker_handler(self, marker=None, scope='All'):
        if marker:
            response = self.client.list_policies(
                Scope=scope,
                OnlyAttached=True,
                PolicyUsageFilter='PermissionsPolicy',
                Marker=marker)
        else:
            response = self.client.list_policies(
                Scope=scope,
                OnlyAttached=True,
                PolicyUsageFilter='PermissionsPolicy'
            )
        return response

    def get_policy_document(self, arn, version_id):
        response = self.client.get_policy_version(PolicyArn=arn, VersionId=version_id)
        document = response['PolicyVersion']['Document']
        return document

    def get_policies(self):
        policies = []
        marker = None
        for scope in ['AWS', 'Local']:
            while True:
                resp = self._marker_handler(marker, scope)
                for policy in resp['Policies']:
                    policy['Scope'] = scope
                    policies.append(policy)
                marker = resp.get('Marker')
                if not resp['IsTruncated']:
                    break
        return policies