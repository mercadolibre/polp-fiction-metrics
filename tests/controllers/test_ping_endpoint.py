from flask import url_for


def test_ping(client):
    response = client.get(url_for("ping.main"))
    assert response.status_code == 200
