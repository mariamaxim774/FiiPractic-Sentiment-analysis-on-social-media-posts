from flask import Blueprint
from controllers.post_controller import *
from services.post_services import sentiment_chart,sentiment_length_chart
posts_routes = Blueprint("posts_routes", __name__)

@posts_routes.route('/posts', methods=['GET'])
def list_posts():
    return get_posts()

@posts_routes.route('/posts', methods=['POST'])
def create_post():
    return add_post()

@posts_routes.route('/posts/sentiments', methods=['GET'])
def list_sentiments():
    return get_sentiments()


@posts_routes.route('/posts/<uuid:post_id>', methods=['GET'])
def list_post_by_id(post_id):
    return get_post_by_id(post_id)


@posts_routes.route('/posts/<uuid:post_id>', methods=['PUT'])
def update_post_by_id(post_id):
    return put_post_by_id(post_id)


@posts_routes.route('/posts/<uuid:post_id>', methods=['DELETE'])
def remove_post_by_id(post_id):
    return delete_post_by_id(post_id)

@posts_routes.route('/posts/<uuid:post_id>/sentiment', methods=['GET'])
def list_sentiments_by_id(post_id):
    return get_sentiments_by_id(post_id)


@posts_routes.route('/posts/<uuid:post_id>/comments', methods=['GET'])
def list_comments(post_id):
    return get_commments(post_id)


@posts_routes.route('/posts/<uuid:post_id>/comments', methods=['POST'])
def create_comments(post_id):
    return post_commments(post_id)


@posts_routes.route('/posts/<uuid:post_id>/like', methods=['POST'])
def create_like(post_id):
    return like_post(post_id)


@posts_routes.route('/posts/<uuid:post_id>/likes', methods=['GET'])
def list_likes(post_id):
    return get_likes(post_id)


@posts_routes.route('/posts/<uuid:post_id>/heart', methods=['POST'])
def create_heart(post_id):
    return love_post(post_id)


@posts_routes.route('/posts/<uuid:post_id>/hearts', methods=['GET'])
def list_hearts(post_id):
    return get_hearts(post_id)

@posts_routes.route('/posts/addposts', methods=['POST'])
def posts():
    return add_posts()

@posts_routes.route('/posts/sentiment-chart', methods=['GET'])
def get_sentiment_chart():
    return sentiment_chart()

@posts_routes.route('/posts/sentiment-length-chart', methods=['GET'])
def get_sentiment_overtime_chart():
    return sentiment_length_chart()