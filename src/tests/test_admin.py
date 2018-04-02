from flask import url_for
from datetime import datetime
import pytest


@pytest.mark.usefixtures('db')
class TestAdmin:

    def test_can_retrieve_index(user, client, post):
        client.login_user()
        resp = client.get(url_for('admin.index'))
        assert resp.status_code == 200
