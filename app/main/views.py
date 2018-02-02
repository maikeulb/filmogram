from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app
)
from flask_login import current_user, login_required
from app.extensions import login, db, images
from app.main import main
from app.main.forms import (
    UploadForm,
    EditProfileForm,
)
from app.models import Post, User
from werkzeug.utils import secure_filename


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('main/index.html',
                           title='Explore',
                           posts=posts)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['photo']
        filename = images.save(file)
        url = images.url(filename)
        post = Post(caption=form.photo_description.data,
                    photo_filename=filename,
                    photo_url=url)

        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    return render_template('main/upload.html',
                           title='Upload',
                           form=form)


@main.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc())
    return render_template('main/profile.html',
                           title='User',
                           user=user,
                           posts=posts)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        file = request.files['profile_img']
        filename = images.save(file)
        url = images.url(filename)
        current_user.profile_img_url = url
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio
    return render_template('main/edit_profile.html',
                           title='Edit Profile',
                           form=form)
