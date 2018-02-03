from app.extensions import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    caption = db.Column(db.String(140))
    photo_filename = db.Column(db.String)
    photo_url = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

#     def followed_posts(self):
#         followed = Post.query.join(
#             followers, 
#             (followers.c.followed_id == Post.user_id)).filter(
#                 followers.c.follower_id == self.id)
#         own = Post.query.filter_by(user_id=self.id)
#         return followed.union(own).order_by(Post.timestamp.desc())
