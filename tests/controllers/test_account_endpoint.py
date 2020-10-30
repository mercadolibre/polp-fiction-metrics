from flask import url_for
from datetime import datetime
from unittest import mock
from unittest.mock import patch,Mock, MagicMock


@patch("app.models.db.db")
@patch("app.controllers.accounts.Organization")
def test_accounts(mock_org, mock_db, client):
    mock_org.return_value.get_accounts.side_effect = Exception()
    response = client.post(url_for("accounts.post"))
    assert response.status_code == 503

@patch("app.controllers.accounts.Account")
@patch("app.controllers.accounts.db")
@patch("app.controllers.accounts.Organization")
def test_accounts_200(mock_org, mock_db, mock_acc, client):
    mock_org.return_value.get_accounts.return_value = {"123":"cloudsec", "456":"testing"}
    response = client.post(url_for("accounts.post"))
    assert response.status_code == 201


