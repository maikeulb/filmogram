import pytest
import json
from flask import url_for


@pytest.mark.usefixtures('db')
class TestPostApi:
    def test_get_posts(self, client, user, post):
        client.login_user()
        resp = client.get(url_for('api.get_posts'))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 200
        assert data is not None

    def test_delete_posts(self, client, user, post):
        client.login_user()
        resp = client.delete(url_for('api.delete_post', id=post.id))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 200
        assert data is not None


@pytest.mark.usefixtures('db')
class TestNotificationApi:

    def test_get_notifications(self, client, user):
        client.login_user()
        resp = client.get(url_for('api.get_notifications'))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 200
        assert data is not None

    def test_reset_notifications(self, client, user, post):
        client.login_user()
        resp = client.delete(url_for('api.reset_notifications', id=post.id))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 200
        assert data is not None


@pytest.mark.usefixtures('db')
class TestLikesApi:

    def test_like(self, client, user, post):
        client.login_user()
        resp = client.post(url_for('api.like', id=post.id))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 201
        assert data['result'] == user.username

    def test_like_404(self, client, user, post):
        client.login_user()
        resp = client.post(url_for('api.like', id=99))
        assert resp.status_code == 404

    def test_unlike(self, client, post, user):
        client.login_user()
        resp = client.delete(url_for('api.unlike', id=post.id))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 201
        assert data['result'] == user.username

    def test_unlike_404(self, client, post, user):
        client.login_user()
        resp = client.delete(url_for('api.unlike', id=99))
        assert resp.status_code == 404


@pytest.mark.usefixtures('db')
class TestFollowingsApi:

    def test_follow(self, client, post, user, second_user):
        client.login_user()
        resp = client.post(url_for('api.follow',
                                   username=second_user.username))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 201
        assert data['result'] == second_user.username

    def test_follow_404(self, client, post, user, second_user):
        client.login_user()
        resp = client.post(url_for('api.follow',
                                   username='unknown_user'))
        assert resp.status_code == 404

    def test_unfollow(self, client, post, user, second_user):
        client.login_user()
        resp = client.delete(url_for('api.unfollow',
                                     username=second_user.username))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 201
        assert data['result'] == second_user.username

    def test_unfollow_404(self, client, post, user, second_user):
        client.login_user()
        resp = client.post(url_for('api.unfollow',
                                   username='unknown_user'))
        assert resp.status_code == 404

    def test_follow_cannot_follow_self(self, client, post, user):
        client.login_user()
        resp = client.post(url_for('api.follow',
                                   username=user.username))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 422

    def test_unfollow_cannot_unfollow_self(self, client, post, user):
        client.login_user()
        resp = client.delete(url_for('api.unfollow',
                                     username=user.username))
        data = json.loads(resp.get_data(as_text=True))
        assert resp.status_code == 422


# @pytest.mark.usefixtures('db')
# class TestCommentsApi:

    # @pytest.mark.skip(reason="need comment factory")
    # def test_can_comment(self, client, post, user, second_user):
    #     client.login_user()
    #     resp = client.post(url_for('api.follow',
    #                                id=comment.id)
    #     data=json.loads(resp.get_data(as_text=True))

    # @pytest.mark.skip(reason="need to make factory for demo user")
    # def test_invalid_comment_demo(self, client, post, user, second_user):
    #     client.login_user()
    #     resp=client.post(url_for('api.follow',
    #                                id=comment.id)
    #     data=json.loads(resp.get_data(as_text=True))
    #     assert resp.status_code == 400
