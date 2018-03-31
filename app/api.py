#Routes and API

from app import db, app
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from .models import User, Task

def set_password(password, salt):
    """Hash and salt the password"""
    db_password = password+salt
    h = sha256_crypt.hash(db_password)
    return h

@app.route('/signup')
def sign_up_page():
    """Redirect to sign up page"""
    return render_template('signup.html')

@app.route('/login')
def login_page():
    """Redirect to login page"""
    return render_template('login.html')

@app.route('/signup', methods=["POST"])
def create_user():
    """Create new user"""
    # Check if the username is taken
    user = db.session.query(User).filter(User.username==request.form['username']).first()
    # If the username is available, then create the user
    if not user:
        user = User(
            username=request.form['username'],
            password=set_password(request.form['password'], request.form['username'])
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    # If the username is unavailable, then flash message and refresh page
    else:
        flash('Username already existed!')
        return render_template('signup.html')

@app.route('/')
def index():
    """Render Homepage/Kanban board"""
    # If not logged in yet, then redirect to login page
    if not session.get('username'):
        return redirect(url_for('login_page'))
    # If logged in, then get the kanban board of the user
    else:
        tasks = db.session.query(Task).filter(Task.username==session.get('username'))
        to_do, doing, done = [],[],[]
        for task in tasks:
            if task.status == 'to_do':
                to_do.append(task)
            elif task.status == 'doing':
                doing.append(task)
            elif task.status == 'done':
                done.append(task)
    return render_template('index.html', to_do=to_do, doing=doing, done=done, user=session.get('username'))

@app.route('/login', methods=['POST'])
def login():
    """User login"""
    user = db.session.query(User).filter(User.username==request.form['username']).first()
    h = request.form['password']+request.form['username']
    # Check if username is registered, if not then flash message
    if not user:
        flash('Invalid username!')
    # If username is in the database, then check password.
    # If the password matches, then log in
    elif sha256_crypt.verify(h, user.password):
        session['username'] = user.username
        flash('Logged in successfully!')
    # If the password does not match, then flash message
    else:
        flash('Incorrect password!')
    return redirect(url_for('index'))

@app.route('/logout')
def log_out():
    """User log out"""
    # Remove the username from the session
    session.pop('username', None)
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add():
    """Add new task"""
    # Need to be logged in to add task
    if not session.get('username'):
        abort(401)
    # If logged in, then add task to the database
    to_do = Task(
        username=session.get('username'),
        task=request.form['task'],
        status='to_do'
    )
    db.session.add(to_do)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/task/<id>/<status>')
def change_status(id,status):
    """Change status of task"""
    # Need to be logged in to change the status of task
    if not session.get('username'):
        abort(401)
    task = db.session.query(Task).filter(Task.id==int(id)).first()
    # If the task does not exist, abort
    if not task:
        abort(404)
    # Else, update the status
    task.status = status
    db.session.commit()  
    return redirect(url_for('index'))

@app.route('/task/<id>', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    """ Delete task"""
    # Need to be logged in to change the status of task
    if not session.get('username'):
        abort(401)
    task = db.session.query(Task).filter(Task.id==int(id)).first()
    # If the task does not exist, abort
    if not task:
        abort(404)
    # Else, delete the status from database
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)