from factory import PostGenerationMethodCall, Sequence, SubFactory
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
    # role = SubFactory(UserFactory)

    class Meta:
        model = User


class PostFactory(BaseFactory):
    id = Sequence(lambda n: n)
    caption = Sequence(lambda n: 'caption{0}'.format(n))
    photo_filename = Sequence(lambda n: 'filename{0}'.format(n))
    photo_url = Sequence(lambda n: 'filename_url{0}'.format(n))
    user_id = Sequence(lambda n: n)
    # user = SubFactory(UserFactory)

    class Meta:
        model = Post


class CommentFactory(BaseFactory):
    id = Sequence(lambda n: n)
    body = Sequence(lambda n: 'body{0}'.format(n))
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    class Meta:
        model = Comment


class NoficationFactory(BaseFactory):
    id = Sequence(lambda n: n)
    name = Sequence(lambda n: 'name{0}'.format(n))
    payload_json = Sequence(lambda n: 'payload{0}'.format(n))
    user = SubFactory(UserFactory)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    class Meta:
        model = Notification


class UserNoficiationFactory(BaseFactory):
    id = Sequence(lambda n: n)
    body = Sequence(lambda n: 'body{0}'.format(n))
    sender = SubFactory(UserFactory)
    recipient = SubFactory(UserFactory)
    # sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # recipient_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    class Meta:
        model = UserNotification
