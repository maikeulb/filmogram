import sys
from flask import (
    jsonify,
)
from app.extensions import db
from app.api import api
from app.models import (
    Post,
)


@api.route('/posts')
def get_posts():
    posts = Post.query.all()
    response = jsonify([post.to_dict() for post in posts])
    return response, 200


@api.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    response = jsonify({'data': 'success'})
    return response, 200
