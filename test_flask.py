from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = True

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class UserViewsTestCase(TestCase):
    """Tests view functions for Users."""

    def setUp(self):
        """Adds sample user."""

        db.drop_all()
        db.create_all()

        user = User(first_name="Annie", last_name="Clark", image_url="https://www.rollingstone.com/wp-content/uploads/2018/06/rs-14399-20140212-stvincent-x1800-1392221859.jpg?resize=1800,1200&w=1800")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clear test DB of added test user."""

        db.session.rollback()

    def test_homepage(self):
        """Tests the homepage loads correctly"""

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Welcome to the Blogly App!</h2>', html)

    def test_list_all_users(self):
        """Tests /users route and that users are displayed"""

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>All Users</h2>', html)
            self.assertIn(f'<li>Annie Clark  <a href="/users/{ self.user_id }">show details</a></li>', html)

    def test_new_user_form(self):
        """Tests /users/new route and that new user form is displayed"""

        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Create a User</h2>', html)
            
    def test_show_user_detail(self):
        """Tests /users route and that users are displayed"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Annie Clark</h2>', html)
            

    def test_new_user_form(self):
        """Tests /users route and that users are displayed"""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Edit User Profile</h2>', html)
            

class PostViewsTestCase(TestCase):
    """Tests view functions for Posts."""

    def setUp(self):
        """Drops, then adds tables, as well as create a sample user and post for testing."""

        db.drop_all()
        db.create_all()

        user = User(first_name="Annie", last_name="Clark", image_url="https://www.rollingstone.com/wp-content/uploads/2018/06/rs-14399-20140212-stvincent-x1800-1392221859.jpg?resize=1800,1200&w=1800")

        db.session.add(user)
        db.session.commit()

        post = Post(title="Post #1", content="This is the content of post #1.", user_id=1)
        

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clear test DB of added test user."""

        db.session.rollback()

    def test_post_on_user_page(self):
        """Tests that posts are being listed on user's detail page."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            post = Post.query.get(1)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{ post.title }', html)

    def test_new_post_form(self):
        """"Tests new post form displays correctly."""

        with app.test_client() as client:
            resp = client.get(f"/users/{ self.user_id }/posts/new")
            html = resp.get_data(as_text=True)
            post = Post.query.get(1)
            user = User.query.get(self.user_id)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h2>Add Post for { user.first_name } { user.last_name }</h2>', html)

    def test_view_post_detail(self):
        """"Tests post detail view displays correctly."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/{self.post_id}")
            html = resp.get_data(as_text=True)
            post = Post.query.get(1)
            user = User.query.get(self.user_id)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h2>{ post.title }</h2>', html)

    def test_view_edit_post(self):
        """"Tests edit post view displays correctly."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Edit Post</h2>', html)