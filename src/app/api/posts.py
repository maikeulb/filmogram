import sys
from flask import (
    jsonify,
)
from flask_login import login_required
from app.api import api
from app.extensions import db
from app.decorators import demo_admin_required, admin_required
from app.models import (
    Post,
)


@api.route('/posts')
@login_required
@demo_admin_required
def get_posts():
    posts = Post.query.all()

    response = jsonify([post.to_dict() for post in posts])
    return response, 200


@api.route('/posts/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()

    response = jsonify({'data': 'success'})
    return response, 200
