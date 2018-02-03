from app.extensions import db
from datetime import datetime


likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    caption = db.Column(db.String(140))
    photo_filename = db.Column(db.String)
    photo_url = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    likes = db.relationship(
        'User',
        secondary=likes
        primaryjoin=(likes.c.user_id == id),
        secondaryjoin=(likes.c.post_id == id),
        backref=db.backref('likes', lazy='joined'),
        lazy='dynamic'
    )

    def like(self, user):
        if not self.has_liked(user):
            self.likes.append(user)

    def unlike(self, user):
        if self.has_liked(user):
            self.likes.remove(user)

    def has_liked(self, user):
        return self.likes.filter(
            likes.c.user_id == user.id).count() > 0
