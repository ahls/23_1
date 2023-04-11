"""Blogly application."""
from flask import Flask, request, render_template,redirect, flash, session
#from flask_debugtoolbar import DebugToolBarExtension
from models import db, connect_db, User, update_user, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hehe123'
#debug= DebugToolBarExtension(app)
connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/users')
def users_list_page():
    users =  User.query.all()
    return render_template('usersList.html', users = users)

@app.route('/users/new', methods=['GET'])
def add_user_page():
    return render_template('addUser.html')

@app.route('/users/new', methods=['POST'])
def on_add_user_page():
    newUser = User(first_name = request.form['first_name'],last_name = request.form['last_name'],image_url = request.form['image_url'])
    db.session.add(newUser)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:userID>/edit', methods=['POST'])
def edit_user_page_post(userID):
    update_user(userID, request.form)

    return redirect(f'/users/{userID}')

@app.route('/users/<int:userID>/edit', methods=['GET'])
def edit_user_page_get(userID):
    user = User.query.get_or_404(userID)
    return render_template('editUser.html',user = user)

@app.route('/users/<int:userID>/delete')
def delete_user_page(userID):
    user = User.query.get_or_404(userID)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:userID>')
def user_detail_page(userID):
    user = User.query.get_or_404(userID)
    posts = user.posts
    return render_template('userDetail.html',user = user,posts = posts)

#post related

@app.route('/users/<int:userID>/posts/new')
def post_new_get(userID):
    user = User.query.get_or_404(userID)
    return render_template('postUpload.html',user = user)

@app.route('/users/<int:userID>/posts/new', methods=['POST'])
def post_new_post(userID):
    newPost = Post(title = request.form['postTitle'],content = request.form['postContent'], author_id = userID, created_at = datetime.now())
    db.session.add(newPost)
    db.session.commit()
    return redirect(f'/posts/{newPost.id}')

@app.route('/posts/<int:postID>')
def post_list_page(postID):
    post = Post.query.get_or_404(postID)
    user = post.author
    return render_template('post.html',post = post, user = user)

@app.route('/posts/<int:postID>/delete', methods=['POST'])
def delete_post(postID):
    post = Post.query.get_or_404(postID)
    userID = post.author_id
    Post.query.filter_by(id=postID).delete()
    db.session.commit()
    return redirect(f'/users/{userID}')

@app.route('/posts/<int:postID>/edit', methods=['GET'])
def edit_post_get(postID):
    post = Post.query.get_or_404(postID)
    user = post.author
    return render_template('postEdit.html',post = post, user = user)


@app.route('/posts/<int:postID>/edit', methods=['POST'])
def edit_post_post(postID):
    post = Post.query.get_or_404(postID)
    post.title = request.form['postTitle']
    post.content = request.form['postContent']
    db.session.add(post)
    db.session.commit()    
    return redirect(f'/posts/{postID}')




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')