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


@api.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    # if user is None:
        # flash('User not found.')
        # return jsonify({'result': 'error'}), 400
    if user == current_user:
        flash('You cannot follow yourself!')
        return jsonify({'result': 'error'}), 422
    current_user.follow(user)
    db.session.commit()
    response = jsonify({'result': user.username})
    return response, 201


@api.route('/follow/<username>', methods=['DELETE'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    # if user is None:
        # return jsonify({'result': 'error'}), 400
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return jsonify({'result': 'error'}), 422
    current_user.unfollow(user)
    db.session.commit()
    response = jsonify({'result': user.username})
    return response, 201
