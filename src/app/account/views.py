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
    login_required,
    current_user,
)
from app.account import account
from app.account.forms import (
    LoginForm,
    RegistrationForm
)
from app.models import User
from app.extensions import login, db


@account.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('account.login'))
        login_user(user)
        return redirect(url_for('posts.index'))

    return render_template('account/login.html',
                           title='Sign In',
                           form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))


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
