from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request
)
from werkzeug.urls import url_parse
from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)
from werkzeug.urls import url_parse
from app.github import github
from app.account.forms import (
    LoginForm,
    RegistrationForm
)
from app.models import User
from app.extensions import login, db


@github.route('/', methods=['GET', 'POST'])
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        return '{}'.format(account_info_json['login'])
    return 'request failed'


@account.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('posts.index'))


@account.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('account.login'))
    return render_template('account/register.html',
                           title='Register',
                           form=form)
