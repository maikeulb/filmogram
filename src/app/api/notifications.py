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
# from app.api.forms import (
    # CommentForm,
# )
from app.models import (
    Post,
    Comment,
)


@api.route('/notifications')
@login_required
def get_notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    response = jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
    return response

@api.route('/notifications', methods=['DELETE'])
@login_required
def reset_notifications():
    current_user.last_user_notification_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    return jsonify({'result': 'success'})
