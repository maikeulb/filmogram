from app.extensions import db
from datetime import datetime, timedelta
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from app.extensions import bcrypt, login
from app.models.post import Post
from app.models.notification import Notification
from app.models.user_notification import UserNotification
import jwt
import sys
import json


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
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=True)
    bio = db.Column(db.String(140))
    profile_img_url = db.Column(db.String)
    last_user_notification_read_time = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

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
        backref=db.backref('followers', lazy='joined'),
        lazy='dynamic'
    )
    likes = db.relationship(
        'Post',
        secondary=likes,
        primaryjoin=(likes.c.user_id == id),
        backref=db.backref('likes', lazy='joined'),
        lazy='dynamic'
    )
    comments = db.relationship(
        'Comment',
        backref='author',
        lazy='dynamic'
    )
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy='dynamic'
    )
    user_notification_sent = db.relationship(
        'UserNotification',
        foreign_keys='UserNotification.sender_id',
        backref='author',
        lazy='dynamic'
    )
    user_notification_received = db.relationship(
        'UserNotification',
        foreign_keys='UserNotification.recipient_id',
        backref='recipient',
        lazy='dynamic'
    )

    def __init__(self, username, email, role=None, password=None, **kwargs):
        super(User, self).__init__(**kwargs)
        if role:
            self.role = role
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def can(self, permissions):
        return self.role.permissions >= permissions

    def is_demo_admin(self):
        return self.can(Permission.DEMO_ADMINISTER)

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

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
        if self.followed:
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
        if self.likes:
            return self.likes.filter(
                likes.c.post_id == post.id).count() > 0

    def liked_posts(self):
        liked = Post.query.join(
            likes,
            (likes.c.post_id == Post.id)) \
            .filter(
            likes.c.user_id == self.id)
        return liked.order_by(Post.timestamp.desc())

    def new_messages(self):
        last_read_time = self.last_user_notification_read_time or datetime(
            1900, 1, 1)
        return UserNotification.query.filter_by(recipient=self).filter(
            UserNotification.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        if self.notifications:
            self.notifications.filter_by(name=name).delete()
            n = Notification(
                name=name, payload_json=json.dumps(data), user=self)
            db.session.add(n)
            return n

    def get_my_following(self):
        my_following = self.query.join(
            followers,
            (followers.c.followed_id == User.id)) \
            .filter(followers.c.follower_id == self.id)
        print(my_following, sys.stdout)
        return my_following

    def get_my_followers(self):
        my_followers = self.query.join(
            followers,
            (followers.c.follower_id == User.id)) \
            .filter(followers.c.followed_id == self.id)
        print(my_followers, sys.stdout)
        return my_followers

    @property
    def follower_count(self):
        if self.followers:
            return len(self.followers)
        return 0

    @property
    def followed_count(self):
        if self.followed and self.followed.all():
            return len(self.followed.all())
        return 0


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False

    def is_demo_admin(self):
        return False


class Permission:
    GENERAL = 0
    DEMO_ADMINISTER = 1
    ADMINISTER = 2


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'DemoAdministrator': (Permission.DEMO_ADMINISTER, 'demo_admin', False),
            'Administrator': (Permission.ADMINISTER, 'admin', False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
