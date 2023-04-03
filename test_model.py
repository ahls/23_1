from unittest import TestCase

from app import app
from models import db, User,update_user

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

class ModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("CREATED TEH TABLE RIGHT HERE")

    def setUp(self):
        with app.app_context():
            print("RESETTING RIGHT HERE")
            self.user = None
            User.query.delete()
            db.session.commit()
    
    def tearDown(self):    
        with app.app_context():
            db.session.rollback()
    
    def create_test_model(self):
        self.user = User(first_name = 'test', last_name = 'case')
        db.session.add(self.user)
        db.session.commit()

    def test_model_add(self):
        with app.app_context():
            self.create_test_model()

            userQ = User.query.first()
            self.assertEqual(self.user, userQ)
    def test_model_update(self):
        with app.app_context():
            self.create_test_model()
            form = {'first_name':'aa','last_name':'bb'}
            update_user(self.user.id,form)

            self.assertEqual(self.user.first_name, 'aa')
            self.assertEqual(self.user.last_name, 'bb')
            

            
