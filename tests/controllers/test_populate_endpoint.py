from flask import url_for
from unittest import mock
from unittest.mock import patch,Mock

@patch("app.controllers.populate.Account")
@patch("app.controllers.populate.db")
@patch("app.controllers.populate.IAM")
@patch("app.controllers.populate.PolicyUpdater")
def test_accounts_500(mock_policy_updater, mock_iam, mock_db, mock_acc, client):
    mock_acc.query.filter_by.side_effect = Exception()
    response = client.post(url_for("populates.post"))
    assert response.status_code == 500

@patch("app.controllers.populate.AccessUpdater")
@patch("app.controllers.populate.IAM")
@patch("app.controllers.populate.Permission")
@patch("app.controllers.populate.Policy")
@patch("app.controllers.populate.Account.query")
@patch("app.controllers.populate.Account")
@patch("app.controllers.populate.db")
@patch("app.controllers.populate.IAM")
@patch("app.controllers.populate.PolicyUpdater")
@patch("app.controllers.populate.UserUpdater")
@patch("app.controllers.populate.RoleUpdater")
def test_accounts_200(
    mock_role_up,
    mock_user_up,
    mock_policy_updater,
    mock_iam,
    mock_db,
    a,
    mock_acc,
    ma,
    c,
    e,
    mock_access_updater,
    client
    ):
    mock_acc.all.return_value = [1,2,3]
    response = client.post(url_for("populates.post"))
    assert response.status_code == 200
