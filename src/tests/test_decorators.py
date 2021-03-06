import pytest
from flask import url_for
from app.decorators import (
    admin_required,
    demo_admin_required
)


class MethodCalled(Exception):
    pass


class TestDecorators:

    def test_admin_decorator(self, client, user):
        client.login_user()

        @admin_required
        def method():
            raise MethodCalled

        with pytest.raises(MethodCalled):
            method()

    def test_demo_admin_decorator(self, client, user):
        client.login_user()

        @demo_admin_required
        def method():
            raise MethodCalled

        with pytest.raises(MethodCalled):
            method()
