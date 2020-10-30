from policyuniverse.arn import ARN

class TrustRelationshipParser():

    def __init__(self, assume_role_policy_document):
        self.document = assume_role_policy_document
    
    def _get_trusted_principals(self, principal_type):
        principal_names = []
        for statement in self.document['Statement']:
            principals = statement['Principal'].get(principal_type)
            if principals:
                principal_names += principals if isinstance(principals, list) else [principals]
        return list(set(principal_names))

    def get_trusted_services_names(self):
        return list(map(lambda x: x.split('.amazonaws.com')[0], self._get_trusted_principals('Service')))
        
    def get_trusted_principal_arns(self, resource_type):
        principals = list(filter(lambda x: ARN(x).name, self._get_trusted_principals('AWS')))
        return [ ARN(principal) for principal in principals if ARN(principal).name.split('/')[0] == resource_type ]
 
    def get_trusted_accounts_uuids(self):
        accounts = self.get_trusted_principal_arns('root')
        return [ principal_policy_universe.account_number for principal_policy_universe in accounts ]

    def is_compliant_for_external_entities(self):
        """
            In order to be compliant to trust external entities it should have an ExternalId and no more than one statement in the policy
        """
        statement = self.document.get('Statement')
        if len(statement)==1 and statement[0].get('Condition',{}).get('StringEquals',{}).get('sts:ExternalId',{}) != {}:
            return True
        return False

    # def get_trusted_services(self):
    #     pass

    # def get_trusted_roles(self):
    #     pass
 
    # def get_trusted_users(self):
    #     pass 

    # def get_trusted_accounts(self):
    #     pass
