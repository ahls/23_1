"""Blogly application."""
from flask import Flask, request, render_template,redirect, flash, session
#from flask_debugtoolbar import DebugToolBarExtension
from models import db, connect_db, User, update_user, Post, Tag
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

def add_tag(post, tagID):
    tag = Tag.query.get(tagID) 
    post.tags.append(tag)

@app.route('/')
def homePage():
    return redirect('/users')

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
    flash('user created!','success')
    return redirect('/users')

@app.route('/users/<int:userID>/edit', methods=['POST'])
def edit_user_page_post(userID):
    update_user(userID, request.form)

    flash('user updated!','success')
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
    
    flash('user deleted!','success')
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
    tags = Tag.query.all()
    return render_template('postUpload.html',user = user,tags=tags)

@app.route('/users/<int:userID>/posts/new', methods=['POST'])
def post_new_post(userID):
    newPost = Post(title = request.form['postTitle'],content = request.form['postContent'], author_id = userID, created_at = datetime.now())
    tags = request.form.getlist('tags')
    for tagName in tags:
        add_tag(newPost,tagName)
    db.session.add(newPost)
    db.session.commit()
    flash('post uploaded!','success')
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
    
    flash('post deleted!','success')
    return redirect(f'/users/{userID}')

@app.route('/posts/<int:postID>/edit', methods=['GET'])
def edit_post_get(postID):
    post = Post.query.get_or_404(postID)
    user = post.author
    tags = Tag.query.all()
    return render_template('postEdit.html',post = post, user = user, tags = tags)


@app.route('/posts/<int:postID>/edit', methods=['POST'])
def edit_post_post(postID):
    post = Post.query.get_or_404(postID)
    post.title = request.form['postTitle']
    post.content = request.form['postContent']
    tags = request.form.getlist('tags')
    for tagName in tags:
        add_tag(post,tagName)
    db.session.add(post)
    db.session.commit()    
    flash('post updated!','success')
    return redirect(f'/posts/{postID}')

@app.route('/posts')
def show_all_posts():
    posts = db.session.query(Post.title, User.first_name, User.last_name).join(User).all()
    return render_template('postList.html',posts=posts)

################################################################################

@app.route('/tags')
def tags_list():
    tags = Tag.query.all()
    return render_template('tags.html',tags=tags)

@app.route('/tags/<int:tagID>')
def tag_detail(tagID):
    tags = Tag.query.get_or_404(tagID)
    return render_template('tagDetail.html',tag=tags)

@app.route('/tags/new', methods=['GET'])
def tags_add_GET():
    return render_template('addNewTag.html')

@app.route('/tags/new', methods=['POST'])
def tags_add_POST():
    inputName = request.form['tagName']
    tagDoesntExist = Tag.query.filter(Tag.name==inputName).count() == 0
    if tagDoesntExist:
        newtag = Tag(name=inputName)
        db.session.add(newtag)
        db.session.commit()
    else:
        flash('that name already exists!','error')
    
    return redirect('/tags')

@app.route('/tags/<int:tagID>/delete',methods=['POST'])
def tag_delete(tagID):
    tag = Tag.query.get_or_404(tagID)

    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')


@app.route('/tags/<int:tagID>/edit', methods=['GET'])
def tags_edit_GET(tagID):
    tag = Tag.query.get_or_404(tagID)
    return render_template('editTag.html', tag = tag)

@app.route('/tags/<int:tagID>/edit', methods=['POST'])
def tags_edit_POST(tagID):
    inputName = request.form['tagName']
    tagExist = Tag.query.filter(Tag.name==inputName).count() !=0
    if tagExist:
        flash('that name already exists!','error')
    else:
        tag = Tag.query.get_or_404(tagID)
        tag.name = inputName
        db.session.add(tag)
        db.session.commit()
        flash('tag has been updated!','success')
    
    return redirect(f'/tags/{tagID}')




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')