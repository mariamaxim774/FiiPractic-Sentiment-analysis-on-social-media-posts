import sentiment_service.app
from models import Post,Comment, db
from data_service.diagrams import sentiment_diagram,length_diagram

def create_post(data):
    content = data.get("content")

    if not content:
        raise ValueError("Content cannot be empty")
    if len(content) < 10:
        raise ValueError("Content must be at least 10 characters long.")

    sentiment=sentiment_service.app.analyze_sentiment(content)
    date=data.get("date")
    if date:
        post = Post(content=content,sentiment=sentiment,created_at=date)
    else:
        post = Post(content=content, sentiment=sentiment)
    db.session.add(post)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return {
        "id": post.id,
        "content": post.content,
        "likes": post.likes,
        "hearts": post.hearts,
        "sentiment": post.sentiment,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

def get_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return None

    return {
        "id": post.id,
        "content": post.content,
        "likes": post.likes,
        "hearts": post.hearts,
        "sentiment": post.sentiment,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "comments": get_comments_by_post_id(post.id)
    }


def get_all_posts():
    posts = Post.query.all()
    if not posts:
        return []

    return [{
        "id": post.id,
        "content": post.content,
        "likes": post.likes,
        "hearts": post.hearts,
        "sentiment": post.sentiment,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "comments": get_comments_by_post_id(post.id)
    } for post in posts]


def update_post(post_id, data):
    post = db.session.get(Post, post_id)

    if not post:
        raise ValueError("Post not found")

    if not len(data):
        raise ValueError("Payload cannot be empty")

    content = data.get("content")
    if content or content == "":
        if len(content) < 10:
            print(content, len(content))
            raise ValueError("Content must be at least 10 characters long.")
        post.content = content

    sentiment = data.get("sentiment")
    if sentiment:
        post.sentiment = sentiment
    else:
        post.sentiment=sentiment_service.app.analyze_sentiment(content)
    post.updated_at = db.func.now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return post.to_dict()


def delete_post(post_id):
    post = db.session.get(Post, post_id)

    if not post:
        return {"message": "Post not found"}
    for comment in post.comments:
        db.session.delete(comment)
    db.session.delete(post)

    try:
        db.session.commit()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e

def like_post_by_id(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return None

    post.likes += 1
    db.session.commit()

    return {"message": "You reacted with a like", "likes": post.likes}


def get_post_likes(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return None

    return {"likes": post.likes}


def love_post_by_id(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return None

    post.hearts += 1
    db.session.commit()

    return {"message": "You reacted with a heart", "hearts": post.hearts}


def get_post_hearts(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return None

    return {"hearts": post.hearts}

def get_posts_sentiments():
    posts = Post.query.all()
    if not posts:
        return []
    return [{
        "sentiment": post.sentiment
    } for post in posts]

def get_posts_sentiments_by_id(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return None

    return {"sentiment": post.sentiment}

def  get_comments_by_post_id(post_id):
    comments = db.session.query(Comment).filter(Comment.post_id == post_id).all()
    if not comments:
        return None

    return [comment.to_dict() for comment in comments]

def sentiment_chart():
    posts = get_all_posts()

    return sentiment_diagram(posts)



def sentiment_length_chart():
    posts = Post.query.all()



    data = []
    for post in posts:
        data.append({
            'content': post.content,
            'sentiment': post.sentiment
        })
    return length_diagram(data)
