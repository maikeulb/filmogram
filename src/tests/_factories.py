from factory import (
    PostGenerationMethodCall,
    Sequence,
    SubFactory)
from factory.alchemy import SQLAlchemyModelFactory
from app.extensions import db
from app.models import (
    User,
    Role,
    Post,
    Comment,
    Notification,
    UserNotification
)


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class RoleFactory(BaseFactory):
    id = Sequence(lambda n: n)
    permissions = 1
    index = "admin"
    default = False

    class Meta:
        model = Role


class UserFactory(BaseFactory):
    id = Sequence(lambda n: n)
    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'P@ssw0rd!')
    role_id = Sequence(lambda n: n)

    class Meta:
        model = User


class PostFactory(BaseFactory):
    id = Sequence(lambda n: n)
    caption = Sequence(lambda n: 'caption{0}'.format(n))
    photo_url = Sequence(lambda n: 'filename_url{0}'.format(n))
    user_id = Sequence(lambda n: n)

    class Meta:
        model = Post


class CommentFactory(BaseFactory):
    id = Sequence(lambda n: n)
    body = Sequence(lambda n: 'body{0}'.format(n))
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
    user_id = Sequence(lambda n: n)
    post_id = Sequence(lambda n: n)

    class Meta:
        model = Comment


class NotificationFactory(BaseFactory):
    id = Sequence(lambda n: n)
    name = Sequence(lambda n: 'name{0}'.format(n))
    payload_json = Sequence(lambda n: 'payload{0}'.format(n))
    user_id = Sequence(lambda n: n)

    class Meta:
        model = Notification


class UserNotificationFactory(BaseFactory):
    id = Sequence(lambda n: n)
    body = Sequence(lambda n: 'body{0}'.format(n))
    sender_id = Sequence(lambda n: n)
    recipient_id = Sequence(lambda n: n)

    class Meta:
        model = UserNotification
