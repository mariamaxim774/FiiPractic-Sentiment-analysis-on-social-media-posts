import unittest
import uuid
from models import Post, db
from config import Config
from flask import Flask
from services import (
    create_post, get_post, get_all_posts,
    update_post, delete_post,
    like_post_by_id, love_post_by_id,
    get_post_likes, get_post_hearts
)

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestPostService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.session = db.session

        Post.metadata.create_all(db.engine)

    def tearDown(self):
        self.session.query(Post).delete()
        self.session.commit()

        Post.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_post(self):
        data = {"content": "This is a valid post with more than 10 characters"}
        post_data = create_post(data)

        post = self.session.query(Post).filter_by(id=post_data["id"]).first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, "This is a valid post with more than 10 characters")

    def test_create_post_empty_content(self):
        data = {"content": ""}
        with self.assertRaises(ValueError):
            create_post(data)

    def test_create_post_short_content(self):
        data = {"content": "short"}
        with self.assertRaises(ValueError):
            create_post(data)

    def test_get_post(self):
        post = Post(content="Test post")
        self.session.add(post)
        self.session.commit()

        post_data = get_post(post.id)
        self.assertIsNotNone(post_data)
        self.assertEqual(post_data["content"], "Test post")

    def test_get_post_not_found(self):
        fake_id = uuid.uuid4()
        post_data = get_post(fake_id)  # Assuming this ID doesn't exist
        self.assertIsNone(post_data)

    def test_get_all_posts(self):
        post1 = Post(content="First post")
        post2 = Post(content="Second post")
        self.session.add(post1)
        self.session.add(post2)
        self.session.commit()

        posts_data = get_all_posts()
        self.assertEqual(len(posts_data), 2)

    def test_update_post(self):
        post = Post(content="Initial content")
        self.session.add(post)
        self.session.commit()

        data = {"content": "Updated content", "sentiment": "positive"}
        updated_post = update_post(post.id, data)

        self.assertEqual(updated_post["content"], "Updated content")
        self.assertEqual(updated_post["sentiment"], "positive")

    def test_update_post_not_found(self):
        data = {"content": "Updated content"}
        with self.assertRaises(ValueError):
            fake_id = uuid.uuid4()
            update_post(fake_id, data)  # Assuming this ID doesn't exist

    def test_delete_post(self):
        post = Post(content="Post to delete")
        self.session.add(post)
        self.session.commit()

        post_id = post.id

        response = delete_post(post_id)
        self.assertEqual(response["message"], "Post deleted successfully")

        deleted_post = self.session.query(Post).filter_by(id=post_id).first()
        self.assertIsNone(deleted_post)


def test_delete_post_not_found(self):
    fake_id = uuid.uuid4()
    response = delete_post(fake_id)  # Assuming this ID doesn't exist
    self.assertEqual(response["message"], "Post not found")

    def test_like_post_by_id(self):
        post = Post(content="Post to like")
        self.session.add(post)
        self.session.commit()

        response = like_post_by_id(post.id)
        self.assertEqual(response["message"], "You reacted with a like")
        self.assertEqual(response["likes"], 1)

    def test_get_post_likes(self):
        post = Post(content="Post with likes", likes=5)
        self.session.add(post)
        self.session.commit()

        likes = get_post_likes(post.id)
        self.assertEqual(likes["likes"], 5)

    def test_love_post_by_id(self):
        post = Post(content="Post to love")
        self.session.add(post)
        self.session.commit()

        response = love_post_by_id(post.id)
        self.assertEqual(response["message"], "You reacted with a heart")
        self.assertEqual(response["hearts"], 1)

    def test_get_post_hearts(self):
        post = Post(content="Post with hearts", hearts=3)
        self.session.add(post)
        self.session.commit()

        hearts = get_post_hearts(post.id)
        self.assertEqual(hearts["hearts"], 3)


if __name__ == '__main__':
    unittest.main()