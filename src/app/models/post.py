from app.extensions import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(140), nullable=True)
    photo_filename = db.Column(db.String)
    photo_url = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'caption': self.caption,
            'photo_url': self.photo_url,
            'author': self.author.username,
            'likes': self.likes,
        }
        return data

    def from_dict(self, data):
        for field in ['caption', 'photo_url', 'author',
                      'likes']:
            if field in data:
                setattr(self, field, data[field])
