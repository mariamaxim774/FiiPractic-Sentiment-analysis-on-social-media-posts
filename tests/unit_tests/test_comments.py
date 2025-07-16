import unittest
import uuid
from models import Comment,Post, db
from config import Config
from flask import Flask
from services import (
    create_post,
    create_comment, get_comment, get_all_comments,
    update_comment, delete_comment, get_post,
    get_comment_sentiment_by_id, get_comments_sentiments
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
        Comment.metadata.create_all(db.engine)

        data = {"content": "This is a valid post for testing"}
        self.post_data = create_post(data)

    def tearDown(self):
        self.session.query(Comment).delete()
        self.session.commit()

        Post.metadata.create_all(db.engine)
        Comment.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_comment(self):
        data = "This is a valid comment"
        comment_data = create_comment(data,self.post_data['id'])

        comment = self.session.query(Comment).filter_by(id=comment_data["id"]).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, "This is a valid comment")

    def test_create_comment_empty_content(self):
        data = ""
        with self.assertRaises(ValueError):
            comment_data = create_comment(data, self.post_data['id'])

    def test_create_comment_without_post_id(self):
        data="This is a valid comment"
        post_id=""
        with self.assertRaises(ValueError):
            create_comment(data,post_id)

    def test_create_comment_for_non_existent_post(self):
        data = "This is a valid comment"
        non_existent_post_id = uuid.uuid4()

        with self.assertRaises(ValueError) as context:
            create_comment(data, non_existent_post_id)
        self.assertEqual(str(context.exception), "Cannot create a comment for a non-existent post.")

    def test_get_comment_by_id(self):
        comment = Comment(content="Test comment",post_id=self.post_data['id'])
        self.session.add(comment)
        self.session.commit()

        comment_data = get_comment(comment.id)
        self.assertIsNotNone(comment_data)
        self.assertEqual(comment_data["content"], "Test comment")

    def test_get_post_not_found(self):
        fake_id = uuid.uuid4()
        comment_data = get_comment(fake_id)
        self.assertIsNone(comment_data)

    def test_get_all_posts(self):
        comment1 = Comment(content="First post",post_id=self.post_data['id'])
        comment2 = Comment(content="Second post",post_id=self.post_data['id'])
        self.session.add(comment1)
        self.session.add(comment2)
        self.session.commit()

        comments_data = get_all_comments()
        self.assertEqual(len(comments_data), 2)

    def test_update_comment(self):
        comment = Comment(content="Initial content",post_id=self.post_data["id"])
        self.session.add(comment)
        self.session.commit()

        data = {"content": "This is a beautiful day","sentiment":"Positive"}
        updated_comment = update_comment(comment.id, data)

        self.assertEqual(updated_comment["content"], "This is a beautiful day")
        self.assertEqual(updated_comment["sentiment"], "Positive")

    def test_update_comment_not_found(self):
        data = "Updated content"
        with self.assertRaises(ValueError):
            fake_id = uuid.uuid4()
            update_comment(fake_id, data)

    def test_delete_comment(self):
        comment = Comment(content="Post to delete",post_id=self.post_data["id"])
        self.session.add(comment)
        self.session.commit()

        comment_id = comment.id

        response = delete_comment(comment_id)
        self.assertEqual(response["message"], "Comment deleted successfully")

        deleted_post = self.session.query(Post).filter_by(id=comment_id).first()
        self.assertIsNone(deleted_post)


    def test_delete_comment_not_found(self):
        fake_id = uuid.uuid4()
        response = delete_comment(fake_id)  # Assuming this ID doesn't exist
        self.assertEqual(response["message"], "Comment not found")

if __name__ == '__main__':
    unittest.main()