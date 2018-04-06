import datetime as dt
import pytest
from app.models import Role, User

from ._factories import UserFactory


class TestUserModel:

    def test_set_password(self):
        user = UserFactory()
        user.set_password('password')
        assert user.check_password('password') is True

    def test_can_follow(self, user, second_user):
        user.follow(second_user)
        assert user.is_following(second_user) is True

    def test_can_unfollow(self, user, second_user):
        user.follow(second_user)
        assert user.is_following(second_user) is True
        user.unfollow(second_user)
        assert user.is_following(second_user) is False

    def test_can_like(self, user, post):
        user.like(post)
        assert user.has_liked(post) is True

    def test_can_unlike(self, user, post):
        user.like(post)
        assert user.has_liked(post) is True
        user.unlike(post)
        assert user.has_liked(post) is False

    def test_get_liked_posts(self, user, post):
        user.like(post)
        assert user.has_liked(post) is True
        liked_posts = user.liked_posts()
        assert liked_posts is not None

    def test_get_following(self, user, second_user):
        user.follow(second_user)
        following = second_user.get_my_following()
        assert following is not None

    def test_get_followers(self, user, second_user):
        user.follow(second_user)
        followers = user.get_my_followers()
        assert followers is not None

    def test_get_follower_count(self, user, second_user):
        user.follow(second_user)
        count = second_user.follower_count
        assert count == 1

    def test_get_followed_count(self, user, second_user):
        user.follow(second_user)
        count = user.followed_count
        assert count == 1


class TestPostModel:

    def test_can_to_dict(self, user, post):
        data = post.to_dict()
        assert data['id'] == post.id

    def test_can_from_to_dict(self, user, post):
        data = {}
        data['caption'] = 'my_caption'
        post.from_dict(data)
        assert post.caption == data['caption']

# class TestNotificationModel:

#     def test_get_data(self, notification):
#         data = post.to_dict()
#         assert data['id'] == post.id
