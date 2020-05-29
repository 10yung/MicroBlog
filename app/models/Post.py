from app import db
from app.models.User import User
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        return f'<Post {format(self.body)}>'
