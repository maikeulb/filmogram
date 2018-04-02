import pytest

from app import create_app
from app.extensions import db as _db
from webtest import TestApp
from .factories import UserFactory, PostFactory
from app.models import User, Post, Role


@pytest.fixture
def app():
    _app = create_app('config.TestingConfig')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    return TestApp(app)


@pytest.fixture
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def post(db):
    post = Post(caption='caption',
                photo_filename='filename',
                photo_url='url',
                user_id=1)
    db.session.add(post)
    db.session.commit()
    return post


@pytest.fixture
def user(db):
    role = Role(name='Administrator',
                permissions=2,
                index='admin',
                default=False)
    user = User(username='demo',
                email='demo@example.com',
                bio='fummy bio',
                profile_img_url='dimmy url',
                role_id=1)
    user.set_password('P@ssw0rd!')
    db.session.add(role)
    db.session.add(user)
    db.session.commit()
    return user


# @pytest.fixture
# def role(db):
#     db.session.commit()
#     return role

# @pytest.fixture
# def post(db):
#     post = PostFactory()
#     db.session.commit()
#     return post
