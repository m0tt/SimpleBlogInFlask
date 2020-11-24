from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreatePostForm, EditPostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from flask import request

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = current_user.posts
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post was successfully created!')
    return render_template('create_post.html', title='Create a new post', form=form)

@app.route('/<int:post_id>')
def post(post_id):
    post = Post().query.get(post_id)
    return render_template('post.html', post = post)

@app.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    form = EditPostForm()
    post = Post().query.get(post_id)
    if form.validate_on_submit():       
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Post was successfully updated!')
        return redirect(url_for('edit', post_id = post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body 
    return render_template('edit_post.html', title='Edit Post', form=form, post_id=post.id)

@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = Post().query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post.title), 'success')
    return redirect(url_for('index'))