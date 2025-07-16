from flask import Flask
from config import Config
from .post_routes import posts_routes
from .comments_routes import  comments_routes
from models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, support_credentials=False)

    app.register_blueprint(posts_routes)
    app.register_blueprint(comments_routes)

    app.config.from_object(Config)
    db.init_app(app)

    return app
