from flask import url_for
from datetime import datetime
from app.models import User
import pytest


@pytest.mark.usefixtures('db')
class TestAccount:
    def test_get_register(self, client):
        res = client.get(url_for('account.register'))
        assert res.status_code == 200

    def test_get_login(self, client):
        res = client.get(url_for('account.login'))
        assert res.status_code == 200

    def test_can_register(self, client, user):
        res = client.post(url_for('account.register', data=user))
        assert res.status_code == 200

    def test_can_authenticated_user_register(self, client, user):
        client.login_user()
        res = client.post(url_for('account.register', data=user))
        assert res.status_code == 302

    def test_can_login(self, client, user):
        res = client.post(url_for('account.login', data=user))
        assert res.status_code == 200

    def test_can_authenticated_user_login(self, client, user):
        client.login_user()
        res = client.post(url_for('account.login', data=user))
        assert res.status_code == 302

    def test_can_logout(self, client, user):
        res = client.get(url_for('account.logout'))
        assert res.status_code == 302
