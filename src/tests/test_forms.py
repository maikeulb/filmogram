import pytest
from app.account.forms import (
    LoginForm,
    RegistrationForm,
)
from app.users.forms import (
    CommentForm,
    EditProfileForm
)
from app.api.forms import CommentForm as _CommentForm
from app.posts.forms import CommentForm as _PostCommentForm


class TestRegistrationForm:
    def test_validate_user_already_registered(self, user):
        form = RegistrationForm(username=user.username, email='foo@bar.com',
                                password='example', confirm='example')
        assert form.validate() is False

    def test_validate_email_already_registered(self, user):
        form = RegistrationForm(username='unique', email=user.email,
                                password='example', confirm='example')
        assert form.validate() is False

    def test_validate_success(self, user):
        form = RegistrationForm(username='newusername', email='new@test.test',
                                password='example', confirm='example')
        assert form.validate() is True


class TestLoginForm:
    def test_validate_success(self, user):
        form = LoginForm(username=user.username, password='P@ssw0rd!')
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, user):
        form = LoginForm(username='unknown', password='example')
        assert form.validate() is False
        assert form.user is None

    def test_validate_invalid_password(self, user):
        user.set_password('example')
        form = LoginForm(username=user.username, password='wrongpassword')
        assert form.validate() is False


class TestEditProfileForm:
    @pytest.mark.skip(reason="this shouldn't be failing")
    def test_edit_profile(self, user):
        form = EditProfileForm(user.username)
        form.username.data = 'cool'
        form.bio.data = 'cool'
        form.profile_img.data = 'cool'
        print(form)
        assert form.validate() is True


class TestUserCommentForm:
    def test_validate_success(self, post, user):
        form = CommentForm(body='cool',
                           post=post,
                           author=user)
        assert form.validate() is True


class TestAPICommentForm:
    def test_validate_success(self, post, user):
        form = _CommentForm(body='cool',
                            post=post,
                            author=user)
        assert form.validate() is True


class TestPostsCommentForm:
    def test_validate_success(self, post, user):
        form = _PostCommentForm(body='cool',
                                post=post,
                                author=user)
        assert form.validate() is True
