from flask import jsonify, request


from services import (
    create_comment, get_comment, get_all_comments,
    update_comment, delete_comment,get_post,
    get_comment_sentiment_by_id,get_comments_sentiments
)

def add_comment():
    try:
        data = request.get_json()

        content, post_id = data["content"], data["post_id"]

        post = get_post(post_id)
        if not post:
            raise ValueError(f'Cannot create comment. The post with {post_id} not found.')


        new_comment = create_comment(content,post_id)
        return jsonify(new_comment), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def get_comment_by_id(comment_id):
    comment = get_comment(comment_id)
    if comment:
        return jsonify(comment), 200
    return jsonify({"message": "Comment not found"}), 404


def get_comments():
    comments = get_all_comments()
    if not comments:
        return jsonify({"message": "No comments found"}), 404
    return jsonify(comments), 200


def put_comment_by_id(comment_id):
    try:
        data = request.get_json()
        updated_comment = update_comment(comment_id, data)
        return jsonify(updated_comment), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete_comment(comment_id):
    try:
        comment = get_comment_by_id(comment_id)
        if not comment:
            return jsonify({"message": f'Comment with id: {comment_id} not found.'}), 404

        delete_comment(comment_id)

        return jsonify({"message": f'Comment with id: {comment_id} deleted.'}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def comment_sentiment_by_id(comment_id):
    result = get_comment_sentiment_by_id(comment_id)
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Sentiments couldn't be analized"}), 404

def comment_sentiments():
    result = get_comments_sentiments()
    if result:
        return jsonify(result), 200
    return jsonify({"message": "Sentiments couldn't be analized"}), 404