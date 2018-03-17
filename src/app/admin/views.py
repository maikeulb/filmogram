import sys
from datetime import datetime
from flask import (
    render_template,
    flash, redirect,
    url_for,
    request,
    current_app
)
from flask_login import current_user, login_required
from app.extensions import login, db
from app.decorators import admin_required, demo_admin_required
from app.admin import admin
from app.models import (
    Post
)


@admin.before_request
@login_required
@demo_admin_required
def require_login():
    pass


@admin.route('/')
@admin.route('/index')
def index():
    posts = Post.query.all()
    return render_template('admin/index.html',
                           posts=posts,
                           title='Posts')


@admin.route('/details/<int:post_id>')
def details(id):
    post = Post.query \
        .filter_by(id=id) \
        .first_or_404()

    return render_template('admin/details.html',
                           post=post,
                           title='Post')


@admin.route('/delete/<int:post_id>', methods=['POST'])
def delete(id):
    post = Post.query \
        .filter_by(id=id).first_or_404()

    db.session.delete(post)
    db.session.commit()
    flash('Delete successfully.', 'success')

    return redirect(url_for('admin.index'))
