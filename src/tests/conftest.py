import pytest

from app import create_app
from app.extensions import db as _db
from webtest import TestApp
from .factories import UserFactory, PostFactory


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
def user(db):
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user


@pytest.fixture
def post(db):
    user = UserFactory(password='myprecious')
    post = PostFactory()
    db.session.commit()
    return post
