from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

class DBTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        with app.app_context():
            User.query.delete()
            db.session.commit()
    def tearDown(self):
        with app.app_context():
            db.session.rollback()

    def test_usersListEmpty(self):
        with app.test_client() as client:
            with app.app_context():
                res = client.get('/users')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code,200)
                self.assertEqual(len(User.query.all()),0)
                self.assertNotIn('case, test', html)
           
    def test_usersList(self):
        with app.test_client() as client:
            with app.app_context():
                user = User(first_name = 'test', last_name = 'case')
                db.session.add(user)
                db.session.commit()

                res = client.get('/users')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code,200)
                self.assertEqual(len(User.query.all()),1)
                self.assertIn('case, test', html)
           
    def test_usersDetail(self):
        with app.test_client() as client:
            with app.app_context():
                user = User(first_name = 'test', last_name = 'case')
                db.session.add(user)
                db.session.commit()

                res = client.get('/users/1')
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code,200)
                self.assertEqual(len(User.query.all()),1)
                self.assertIn('<h2>test case</h2>', html)
           