import sys
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app
)
from flask_login import current_user, login_required
from app.extensions import db, images
from app.user import user
from app.user.forms import (
    EditProfileForm
)
from app.models import (
    Post,
    User,
)


@user.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user.profile', username=user.username,
        page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user.profile', username=user.username,
        page=posts.prev_num) if posts.has_prev else None

    return render_template('user/profile.html', 
                           title='User',
                           user=user, 
                           posts=posts.items,
                           next_url=next_url, 
                           prev_url=prev_url)


@user.route('/edit_profile', methods=['GET', 'POST'])
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
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.bio
    return render_template('user/edit_profile.html',
                           title='Edit Profile',
                           form=form)

@user.route('/followers/<username>', methods=['GET', 'POST'])
def followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    followers = user.get_my_followers().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.followers', page=followers.next_num) \
        if followers.has_next else None
    prev_url = url_for('main.followers', page=followers.prev_num) \
        if followers.has_prev else None
    print(followers.items, file=sys.stdout)
    return render_template('user/followers.html',
                           title='Followers',
                           followers=followers.items,
                           next_url=next_url,
                           prev_url=prev_url)


@user.route('/following/<username>', methods=['GET', 'POST'])
def following(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    following = user.get_my_following().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.following', page=following.next_num) \
        if following.has_next else None
    prev_url = url_for('main.following', page=following.prev_num) \
        if following.has_prev else None
    print(following.items, file=sys.stdout)
    return render_template('user/following.html',
                           title='Following',
                           following=following.items,
                           next_url=next_url,
                           prev_url=prev_url)
