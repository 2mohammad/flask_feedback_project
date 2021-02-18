from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_feedback_project_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.init_app(app)

with app.app_context():
    
    db.create_all()


@app.route("/")
def root():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username)
        user = User.authenticate(username, password)
        print("user is:")
        print(user.password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            #session.pop('user_id')
            session['user_id'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            #session.pop('user_id')
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)


@app.route('/users/<user_id>')
def secret(user_id):
    if 'user_id' not in session:
        return redirect('/login')
    else:
        user = User.query.get_or_404(user_id)
        feedbacks = user.feedback
        return render_template('secret.html', user=user, feedbacks=feedbacks)

@app.route('/users/<user_id>/feedback/add', methods=["GET", "POST"])
def add_feedback(user_id):
    username = user_id
    if 'user_id' not in session:
        return redirect('/login')
    else:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = request.form["title"]
            content = request.form["content"]
            new_feedback = Feedback(title=title, content=content, username=username)
            print(new_feedback.content)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:    
            user = User.query.get_or_404(user_id)
            return render_template('add_post.html', user=user, form=form)    

@app.route('/logout')
def logout():
    try:
        session.pop('user_id')
        return redirect('/')
    except:
        return redirect('/')


