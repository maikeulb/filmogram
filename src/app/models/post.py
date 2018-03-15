from app.extensions import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(140))
    photo_filename = db.Column(db.String)
    photo_url = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship(
        'Comment',
        backref='post',
        # lazy='dynamic'
    )

    def to_dict(self):
        data = {
            'likes': self.likes,
        }
        return data
