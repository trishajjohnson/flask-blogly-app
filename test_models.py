from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Cleans up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Cleans up any users created during testing."""

        db.session.rollback()

    def testAddUser(self):
        """Tests whether new User instance is created and added to the DB correctly."""

        user = User(first_name="Trisha", last_name="Johnson", image_url="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/flG3to96dNKSAFlfwDfrkGVifbM=/1440x0/arc-anglerfish-arc2-prod-bostonglobe.s3.amazonaws.com/public/ZUVLSGU6CAI6HKIVAIHMC2KCEM.jpg")

        db.session.add(user)
        db.session.commit()

        user1 = User.query.get_or_404(1)

        self.assertEqual(user1.first_name, "Trisha")
        self.assertEqual(user1.image_url, "https://bostonglobe-prod.cdn.arcpublishing.com/resizer/flG3to96dNKSAFlfwDfrkGVifbM=/1440x0/arc-anglerfish-arc2-prod-bostonglobe.s3.amazonaws.com/public/ZUVLSGU6CAI6HKIVAIHMC2KCEM.jpg")



class PostModelTestCase(TestCase):
    """Test Post Model"""

    def setUp(self):
        """Cleans up any existing posts."""

        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Cleans up any posts created during testing."""

        db.session.rollback()

    def testAddPost(self):
        """Tests whether new Post instance is created and added to the DB correctly."""

        user = User(first_name="Trisha", last_name="Johnson", image_url="https://bostonglobe-prod.cdn.arcpublishing.com/resizer/flG3to96dNKSAFlfwDfrkGVifbM=/1440x0/arc-anglerfish-arc2-prod-bostonglobe.s3.amazonaws.com/public/ZUVLSGU6CAI6HKIVAIHMC2KCEM.jpg")

        db.session.add(user)
        db.session.commit()

        post = Post(title="Post #1", content="This is the content of post #1.", user_id=1)
        
        db.session.add(post)
        db.session.commit()

        post1 = Post.query.get_or_404(1)

        self.assertEqual(post1.title, "Post #1")
        self.assertEqual(post1.user_id, 1)
        self.assertEqual(post1.content, "This is the content of post #1.")