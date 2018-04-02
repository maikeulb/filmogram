from flask import url_for
from datetime import datetime
import pytest


@pytest.mark.usefixtures('db')
class TestPosts:

    def test_auth_required(user, client, post):
        client.login_user()
        resp = client.get(url_for('posts.index'))
        assert resp.status_code == 200
