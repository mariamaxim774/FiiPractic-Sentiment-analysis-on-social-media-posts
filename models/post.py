from datetime import datetime
from . import db
from sqlalchemy import Uuid
import uuid

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(Uuid, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)
    hearts = db.Column(db.Integer, default=0)
    sentiment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    comments = db.relationship("Comment", back_populates="post",cascade="all, delete-orphan",
    passive_deletes=True)

    def __repr__(self):
        return f'<Post {self.id}: {self.content}>'

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes': self.likes,
            'hearts': self.hearts,
            'sentiment': self.sentiment
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
