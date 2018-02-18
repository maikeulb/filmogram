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


@api.route('/comment/<id>', methods=['post'])
def comment(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    print(form, sys.stdout)
    print(post, sys.stdout)
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        print(form.body.data, sys.stdout)
        return jsonify({
            'data': form.body.data})
    return jsonify(data=form.errors)
