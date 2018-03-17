import sys
from datetime import datetime
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
    current_app
)
from flask_login import current_user, login_required
from app.extensions import db
from app.api import api
from app.models import (
    Post,
    User,
    Notification,
    UserNotification
)
import json
from app.api.forms import (
    CommentForm,
)
from app.models import (
    Post,
    Comment,
)


@api.route('/posts')
def get_posts():
    posts = Post.query.all()
    response = jsonify([post.to_dict() for post in posts])
    return response


@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    response = jsonify({'data': 'success'})
    return response
