"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"
    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(30),nullable = False)
    last_name = db.Column(db.String(30),nullable = False)
    image_url = db.Column(db.String(100),nullable = True)
    
    def __repr__(self):
        return f"id:{self.id} name({self.first_name} {self.last_name})"


def update_user(userID,form):
    editingUser = User.query.get_or_404(userID)
    editingUser.first_name = form.get('first_name','')
    editingUser.last_name = form.get('last_name','')
    editingUser.image_url = form.get('image_url','')
    
    db.session.add(editingUser)
    db.session.commit()

