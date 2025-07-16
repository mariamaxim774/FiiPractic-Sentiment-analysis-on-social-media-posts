from models import Comment,Post, db
import sentiment_service.app
import uuid

def create_comment(content, post_id):

    if not content:
        raise ValueError("Content cannot be empty")

    if not post_id :
        raise ValueError("Cannot create a comment without a valid post_id.")

    post = db.session.query(Post).filter_by(id=post_id).first()
    if not post:
        raise ValueError("Cannot create a comment for a non-existent post.")

    sentiment = sentiment_service.app.analyze_sentiment(content)
    comment = Comment(content=content, post_id=post_id,sentiment=sentiment)
    db.session.add(comment)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return comment.to_dict()


def get_comment(comment_id):
    comment =  db.session.get(Comment, comment_id)
    if not comment:
        return None
    return comment.to_dict()


def get_all_comments():
    comments = Comment.query.all()
    if not comments:
        return None
    return [comment.to_dict() for comment in comments]



def update_comment(comment_id, data):
    comment = db.session.get(Comment, comment_id)
    print(data)
    if not comment:
        raise ValueError("comment not found")

    content = data.get("content")
    if content:
        if len(content) < 10:
            raise ValueError("Content must be at least 10 characters long.")
        comment.content = content

    sentiment = data.get("sentiment")
    print(sentiment)
    if sentiment:
        comment.sentiment = sentiment
    else:
        comment.sentiment=sentiment_service.app.analyze_sentiment(content)

    comment.updated_at = db.func.now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return comment.to_dict()

def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)

    if not comment:
        return {"message": "Comment not found"}
    try:
        db.session.delete(Comment.query.get(comment_id))
        db.session.commit()
        return {"message": "Comment deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e

def get_comment_sentiment_by_id(comment_id):
    comment= db.session.get(Comment, comment_id)
    if not comment:
        return None

    return {"sentiment": comment.sentiment}


def get_comments_sentiments():
    comments = Comment.query.all()
    if not comments:
        return []
    return [{
        "sentiment": comment.sentiment
        } for comment in comments]