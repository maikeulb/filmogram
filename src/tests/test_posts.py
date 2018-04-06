from flask import url_for
from datetime import datetime
import pytest
from app.models import Post


@pytest.mark.usefixtures('db')
class TestPosts:

    def test_get_index(self, client, post):
        client.login_user()
        resp = client.get(url_for('posts.index'))
        assert resp.status_code == 200

    def test_get_post(self, client, post):
        client.login_user()
        resp = client.get(url_for('posts.post'))
        assert resp.status_code == 200

    def test_get_favorites(self, client, post):
        client.login_user()
        resp = client.get(url_for('posts.favorites'))
        assert resp.status_code == 200

    def test_can_post(self, client, post):
        client.login_user()
        post = Post(caption='caption',
                    photo_filename='filename',
                    photo_url='url',
                    user_id=1)
        resp = client.post(url_for('posts.post', data=post))
        assert resp.status_code == 200

    # def test_can_login(self, client, user):
    #     res = client.post(url_for('account.register', data=user))
    #     res = client.post(url_for('account.login', data=user))
    #     assert res.status_code == 200

#     def test_get_details(user, client, post):
#         client.login_user()
#         resp = client.get(url_for('posts.details', id=post.id))
#         assert resp.status_code == 200
