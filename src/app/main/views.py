import sys
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    jsonify,
    current_app
)
from flask_login import current_user, login_required
from app.extensions import db, images
from app.main import main
from app.main.forms import (
    CommentForm,
    EditProfileForm,
    UploadForm
)
from app.models import Post, User, Comment


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('main/index.html',
                           title='Followed Posts',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


@main.route('/explore', methods=['GET', 'POST'])
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('main/index.html',
                           title='Explore',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


@main.route('/likes', methods=['GET', 'POST'])
def likes():
    page = request.args.get('page', 1, type=int)
    posts = current_user.liked_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.likes', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.likes', page=posts.prev_num) \
        if posts.has_prev else None
    print(posts.items, file=sys.stdout)
    return render_template('main/index.html',
                           title='Liked',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


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
                    photo_url=url,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    return render_template('main/upload.html',
                           title='Upload',
                           form=form)


@main.route('/user/<username>')
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('main/profile.html', 
                           title='User',
                           user=user, 
                           posts=posts.items,
                           next_url=next_url, 
                           prev_url=prev_url)


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

@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    if user == current_user:
        # flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    # flash('You are following %(username)s!', username=username)
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        # return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    # flash('You are not following %(username)s.', username=username)
    return redirect(url_for('main.user', username=username))


# https://stackoverflow.com/questions/46333738/change-like-status-with-jquery-on-a-flask-app
@main.route('/like/<id>', methods=['GET', 'POST'])
@login_required
def like(id):
    print("hi", sys.stdout)
    post = Post.query.filter_by(id=id).first()
    if post is None:
        # flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    current_user.like(post)
    db.session.commit()
    # flash('You are following %(username)s!', username=username)
    # return redirect(url_for('main.index'))
    return jsonify({'result': 'success'})


@main.route('/unlike/<id>')
@login_required
def unlike(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        # flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    current_user.unlike(post)
    db.session.commit()
    # flash('You are following %(username)s!', username=username)
    return redirect(url_for('main.index'))


@main.route('/details/<id>', methods=['GET', 'POST'])
@login_required
def details(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('main.index'))
    return render_template('main/details.html',
                           title='Details',
                           form=form,
                           post=post)
