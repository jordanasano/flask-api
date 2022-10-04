from unittest import TestCase

from app import app, db
from models import User, Post
from flask import json

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-api-test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last")

        second_user = User(first_name="test_first_two", last_name="test_last_two")

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")

            self.assertEqual(resp.status_code, 200)

            usersJSON = resp.get_data(as_text=True)
            users = json.loads(usersJSON)

            self.assertIn({
                "first_name":"test_first",
                "last_name":"test_last", 
                "id":self.user_id
            }, users)

    def test_create_user(self):
        with self.client as c:
            resp = c.post("/users", 
            json={
                "first_name":"new_first", 
                "last_name":"new_last"
            })

            self.assertEqual(resp.status_code, 201)

            responseJSON = resp.get_data(as_text=True)
            response = json.loads(responseJSON)

            self.assertEqual({"post_user":"successful"}, response)

    def test_delete_user(self):
        with self.client as c:
            resp = c.delete(f'/users/{self.user_id}')

            self.assertEqual(resp.status_code, 200)

            responseJSON = resp.get_data(as_text=True)
            response = json.loads(responseJSON)

            self.assertEqual({"deleted":self.user_id}, response)

            resp2 = c.delete(f'/users/{100000}')

            self.assertEqual(resp2.status_code, 404)
    