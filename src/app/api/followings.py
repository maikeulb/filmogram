import sys
from flask import (
    flash,
    jsonify,
)
from flask_login import current_user, login_required
from app.extensions import db
from app.api import api
from app.models import (
    User,
)


@api.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User not found.')
        return jsonify({'result': 'error'}), 404
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
    if user is None:
        flash('User not found.')
        return jsonify({'result': 'error'}), 404
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return jsonify({'result': 'error'}), 422
    current_user.unfollow(user)
    db.session.commit()
    response = jsonify({'result': user.username})
    return response, 201
