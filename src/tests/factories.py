from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from app.extensions import db
from app.models import User, Post


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    username = Sequence(lambda n: 'user{0}'.format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    is_authenticated = True
    class Meta:
        model = User


class PostFactory(BaseFactory):
    caption = Sequence(lambda n: 'caption{0}'.format(n))
    photo_filename = Sequence(lambda n: 'filename{0}'.format(n))
    photo_url = Sequence(lambda n: 'filename_url{0}'.format(n))
    user_id = 1

    class Meta:
        model = Post
