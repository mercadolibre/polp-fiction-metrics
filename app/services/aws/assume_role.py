import abc
import os
import boto3


class AssumeRoleInterface(abc.ABC):

    @abc.abstractmethod
    def get_client(self, service):
        pass

    @abc.abstractmethod
    def _new_assumed_role_session(self, session, account, role_name):
        pass

class AssumeRole(AssumeRoleInterface):

    def __new__(cls, *args, **kwargs):
        if 'SCOPE' in os.environ and os.environ["SCOPE"] != "single-account":
            print("Assume Role Prod")
            return AssumeRoleProd(*args)
        else:
            return AssumeRoleLocal(*args)

class AssumeRoleLocal(AssumeRoleInterface):

    def __init__(self, account, role_name):
        self.cross_account_role_arn = f"arn:aws:iam::{account}:role/{role_name}"

    def get_client(self, service):
        return boto3.client(service, region_name="us-east-1")

    def _new_assumed_role_session(self, session, role_arn):
        pass

class AssumeRoleProd(AssumeRoleInterface):

    def __init__(self,account, role_name):
        self.cross_account_role_arn = f"arn:aws:iam::{account}:role/{role_name}"

    def get_client(self, service):
        client = self._new_assumed_role_session(
            boto3.Session(),
            self.cross_account_role_arn
            ).client(
                service,
                region_name="us-east-1"
                )
        return client

    def _new_assumed_role_session(self, session, role_arn):
        credentials = session.client('sts').assume_role(
            RoleArn=role_arn,
            RoleSessionName='role_session',
            DurationSeconds=3600)
        return boto3.Session(
            aws_access_key_id=credentials['Credentials']['AccessKeyId'],
            aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
            aws_session_token=credentials['Credentials']['SessionToken'])
