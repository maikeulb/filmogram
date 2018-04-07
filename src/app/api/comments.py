import sys
from flask import (
    jsonify,
)
from flask_login import current_user, login_required
from app.extensions import db
from app.api import api
from app.models import (
    Post,
    Comment
)
from app.api.forms import (
    CommentForm,
)


@api.route('/comment/<id>', methods=['post'])
@login_required
def comment(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        return jsonify({
            'body': form.body.data,
            'author': current_user.username
        })
    return jsonify(data=form.errors), 400
