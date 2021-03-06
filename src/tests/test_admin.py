import pytest
from flask import url_for


@pytest.mark.usefixtures('db')
class TestAdmin:

    def test_get_index(self, client, post):
        client.login_user()
        resp = client.get(url_for('admin.index'))
        assert resp.status_code == 200

    def test_delete_post(self, client, post):
        client.login_user()
        resp = client.post(url_for('admin.delete', post_id=post.id))
        assert resp.status_code == 302
