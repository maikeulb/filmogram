from app.extensions import db
from datetime import datetime, timedelta
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from app.extensions import bcrypt, login
from app.models.post import Post
import jwt
import sys


likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    bio = db.Column(db.String(140))
    profile_img_url = db.Column(db.String)

    posts = db.relationship(
        'Post', 
        backref='author', 
        lazy='dynamic'
    )
    followed = db.relationship(
        'User', 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), 
        lazy='dynamic'
    )
    likes = db.relationship(
        'Post',
        secondary=likes,
        primaryjoin=(likes.c.user_id == id),
        backref=db.backref('likes', lazy='joined'),
        lazy='dynamic'
    )

    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def like(self, post):
        if not self.has_liked(post):
            self.likes.append(post)

    def unlike(self, post):
        if self.has_liked(post):
            self.likes.remove(post)

    def has_liked(self, post):
        return self.likes.filter(
            likes.c.post_id == post.id).count() > 0

    def liked_posts(self):
        liked = Post.query.join(
            likes,
            (likes.c.post_id == Post.id)) \
                .filter(
                likes.c.user_id == self.id)
        print(liked, file=sys.stdout)
        return liked.order_by(Post.timestamp.desc())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
