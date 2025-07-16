from datetime import datetime
from sqlalchemy import Uuid
import uuid
from . import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(Uuid, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    sentiment = db.Column(db.Text)
    post_id = db.Column(Uuid, db.ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    post = db.relationship("Post", back_populates="comments")

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'post_id': self.post_id,
            'sentiment':self.sentiment
        }

    def __repr__(self):
        return f'<Comment {self.id}: {self.content}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
