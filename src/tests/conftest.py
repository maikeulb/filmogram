import pytest

from app import create_app
from app.extensions import db as _db
from webtest import TestApp
from .factories import UserFactory, PostFactory
from app.models import User, Post, Role
from flask.testing import FlaskClient
from flask import Response, url_for
from werkzeug.utils import cached_property


class HtmlTestResponse(Response):
    @cached_property
    def _loc(self):
        return urlparse(self.location)

    @cached_property
    def scheme(self):
        return self._loc.scheme

    @cached_property
    def netloc(self):
        return self._loc.netloc

    @cached_property
    def path(self):
        return self._loc.path or '/'

    @cached_property
    def params(self):
        return self._loc.params

    @cached_property
    def query(self):
        return self._loc.query

    @cached_property
    def fragment(self):
        return self._loc.fragment

    @cached_property
    def html(self):
        return self.data.decode('utf-8')


class HtmlTestClient(FlaskClient):
    def login_user(self):
        return self.login_with_creds('demo', 'P@ssw0rd!')

    def login_admin(self):
        return self.login_with_creds('demo', 'P@ssw0rd!')

    def login_with_creds(self, username, password):
        return self.post(url_for('account.login'),
                         data=dict(username=username, password=password))

    def logout(self):
        self.get('account.logout')


@pytest.fixture
def app():
    _app = create_app('config.TestingConfig')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture()
def client(app):
    app.test_client_class = HtmlTestClient
    app.response_class = HtmlTestResponse
    with app.test_client() as client:
        yield client


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
def post(db, user):
    post = Post(caption='caption',
                photo_filename='filename',
                photo_url='url',
                user_id=user.id)
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


# @pytest.fixture
# def user(db):
#     """A user for the tests."""
#     user = UserFactory(password='myprecious')
#     db.session.commit()
#     return user
