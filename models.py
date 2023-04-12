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

class Post(db.Model):
    """model for posts"""
    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.String(100),nullable = False)
    content = db.Column(db.Text,nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = True)

    author = db.relationship('User',backref=db.backref('posts',cascade="all, delete-orphan"))
    tags = db.relationship('Tag', secondary='posttags', backref='posts')

class Tag(db.Model):
    """model for tags"""
    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    name = db.Column(db.String(100),unique = True,nullable = False)

class PostTag(db.Model):
    __tablename__ = "posttags"

    post_id = db.Column(db.Integer,db.ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True,nullable=False)
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True,nullable=False)