from unittest.mock import MagicMock, Mock
from app.services.aws.assume_role import AssumeRole
import os



def test_assume_instance():
    TEMP_SCOPE = os.environ.get("SCOPE")
    if not TEMP_SCOPE:
        TEMP_SCOPE = "test"
    a = AssumeRole("account","role_name")
    assert a.cross_account_role_arn == "arn:aws:iam::account:role/role_name"
    os.environ["SCOPE"] = "prod"
    a = AssumeRole("account","role_name")
    assert a.cross_account_role_arn == "arn:aws:iam::account:role/role_name"
    os.environ["SCOPE"] = TEMP_SCOPE

