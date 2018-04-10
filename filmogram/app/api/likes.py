import sys
from flask import (
    jsonify,
)
from flask_login import current_user, login_required
from app.extensions import db
from app.api import api
from app.models import (
    Post,
    User,
    UserNotification
)


@api.route('/like/<int:id>', methods=['POST'])
@login_required
def like(id):
    post = Post.query.get_or_404(id)
    current_user.like(post)
    user = User.query.filter_by(id=post.user_id).first_or_404()
    user.add_notification('unread_message_count', user.new_messages())
    notification = UserNotification(
        author=current_user, recipient=user, body=1)
    db.session.add(notification)
    db.session.commit()
    response = jsonify({'result': current_user.username})
    return response, 201


@api.route('/like/<int:id>', methods=['DELETE'])
@login_required
def unlike(id):
    post = Post.query.get_or_404(id)
    current_user.unlike(post)
    db.session.commit()
    response = jsonify({'result': current_user.username})
    return response, 201
