import json
from flask import Response, url_for
from flask.testing import FlaskClient
from urllib.parse import urlparse
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


class ApiTestClient(HtmlTestClient):
    def open(self, *args, **kwargs):
        kwargs['data'] = json.dumps(kwargs.get('data'))

        kwargs.setdefault('headers', {})
        kwargs['headers']['Content-Type'] = 'application/json'
        kwargs['headers']['Accept'] = 'application/json'

        return super().open(*args, **kwargs)


class ApiTestResponse(HtmlTestResponse):
    @cached_property
    def json(self):
        assert self.mimetype == 'application/json', (self.mimetype, self.data)
        return json.loads(self.data)

    @cached_property
    def errors(self):
        return self.json.get('errors', {})
