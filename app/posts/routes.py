from flask import render_template, flash, redirect, url_for
from app import db
from app.posts.forms import CreatePostForm, EditPostForm
from flask_login import current_user, login_required
from app.models import Post
from flask import request
from app.posts import bp


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post was successfully created!')
    return render_template('posts/create_post.html', title='Create a new post', form=form)

@bp.route('/<int:post_id>')
def post(post_id):
    post = Post().query.get(post_id)
    return render_template('posts/post.html', post = post)

@bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    form = EditPostForm()
    post = Post().query.get(post_id)
    if form.validate_on_submit():       
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Post was successfully updated!')
        return redirect(url_for('posts.edit', post_id = post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body 
    return render_template('posts/edit_post.html', title='Edit Post', form=form, post_id=post.id)

@bp.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = Post().query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post.title), 'success')
    return redirect(url_for('main.index'))