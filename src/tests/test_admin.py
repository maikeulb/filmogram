from flask import url_for
from datetime import datetime
import pytest


@pytest.mark.usefixtures('db')
class TestPosts:

    def test_get_index(self, testapp):
        resp = testapp.get(url_for('admin.index'))
        assert resp.status_code == 200
