import pytest
from flask import url_for
from app.models import User


@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_profile(self, client, post):
        client.login_user()
        resp = client.get(url_for('users.profile', username='demo'))
        assert resp.status_code == 200

    def test_get_edit_profile(self, client, post):
        client.login_user()
        resp = client.get(url_for('users.edit_profile'))
        assert resp.status_code == 200

    def test_get_discover(self, client, post):
        client.login_user()
        resp = client.get(url_for('users.discover'))
        assert resp.status_code == 200

    def test_can_edit_profile(self, client, post):
        client.login_user()
        user = User(username='demo',
                    email='demo@example.com',
                    bio='fummy bio',
                    profile_img_url='dimmy url')
        resp = client.post(url_for('posts.upload', data=user))
        assert resp.status_code == 200

    # def test_can_leave_comment(self, client, post):
    #     client.login_user()
    #     resp = client.get(url_for('users.profile', username='demo'))
    #     assert resp.status_code == 200
