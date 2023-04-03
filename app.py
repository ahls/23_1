"""Blogly application."""
from flask import Flask, request, render_template,redirect, flash, session
#from flask_debugtoolbar import DebugToolBarExtension
from models import db, connect_db, User, update_user

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
    User.query.filter_by(id=userID).delete()
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:userID>')
def user_detail_page(userID):
    user = User.query.get_or_404(userID)
    return render_template('userDetail.html',user = user)

    