from flask import Blueprint
from controllers.comments_controller import *

comments_routes = Blueprint("comments_routes", __name__)

@comments_routes.route('/comments', methods=['GET'])
def list_comments():
    return get_comments()

@comments_routes.route('/comments', methods=['POST'])
def create_comment():
    return add_comment()


@comments_routes.route('/comments/<uuid:comment_id>', methods=['GET'])
def list_comment_by_id(comment_id):
    return get_comment_by_id(comment_id)


@comments_routes.route('/comments/<uuid:comment_id>', methods=['PUT'])
def update_comment_by_id(comment_id):
    return put_comment_by_id(comment_id)


@comments_routes.route('/comments/<uuid:comment_id>', methods=['DELETE'])
def remove_comment_by_id(comment_id):
    return delete_comment(comment_id)


@comments_routes.route('/comments/<uuid:comment_id>/sentiment', methods=['GET'])
def list_sentiments_by_id(comment_id):
    return comment_sentiment_by_id(comment_id)

@comments_routes.route('/comments/sentiments', methods=['GET'])
def list_sentiments():
    return comment_sentiments()