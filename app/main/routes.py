from flask import render_template
from app.main import bp
from flask_login import current_user, login_required


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = current_user.posts
    return render_template('index.html', title='Home Page', posts=posts)