import sys
from flask import (
    render_template,
    flash, redirect,
    url_for,
)
from flask_login import login_required
from app.extensions import db
from app.decorators import demo_admin_required
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


@admin.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    post = Post.query \
        .filter_by(id=post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash('Delete successfully.', 'success')

    return redirect(url_for('admin.index'))
