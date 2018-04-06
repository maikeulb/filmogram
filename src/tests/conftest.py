import pytest

from app import create_app
from app.extensions import db as _db
from app.models import User, Post, Role
from webtest import TestApp
from ._client import (
    ApiTestClient,
    ApiTestResponse,
    HtmlTestClient,
    HtmlTestResponse,
)
from ._factories import (
    UserFactory,
    PostFactory,
    RoleFactory
)


@pytest.fixture
def app():
    _app = create_app('config.TestingConfig')
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.yield_fixture
def api_client(app):
    app.response_class = ApiTestResponse
    app.test_client_class = ApiTestClient
    with app.test_client() as client:
        yield client


@pytest.fixture
def client(app):
    app.test_client_class = HtmlTestClient
    app.response_class = HtmlTestResponse
    with app.test_client() as client:
        yield client


@pytest.fixture
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
def post(db, user):
    post = PostFactory(user_id=user.id)
    db.session.commit()
    return post


@pytest.fixture
def comment(db, user):
    comment = CommentFactory(post_id=post.id)
    db.session.commit()
    return comment


@pytest.fixture
def user(db):
    role = RoleFactory(
        name='Administrator',
        permissions=2,
        index='admin',
        default=False)
    db.session.commit()
    user = UserFactory(
        username='demo',
        password='P@ssw0rd!',
        role_id=role.id)
    db.session.commit()
    return user


@pytest.fixture()
def second_user(db):
    role = RoleFactory(
        name='User',
        permissions=0,
        index='user',
        default=False)
    db.session.commit()
    user = UserFactory(
        username='user',
        password='P@ssw0rd!',
        role_id=role.id)
    db.session.commit()
    return user
