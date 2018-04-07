import sys
from flask import (
    current_app,
    render_template,
    redirect,
    request,
    flash,
    url_for,
)
from flask_login import current_user, login_required
from app.extensions import db, images
from app.user import user
from app.user.forms import (
    CommentForm,
    EditProfileForm
)
from app.models import (
    Post,
    User,
    Comment,
)


@user.route('/<username>')
def profile(username):
    form = CommentForm()
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    following = user.get_my_following()
    followers = user.get_my_followers()
    next_url = url_for('user.profile', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user.profile', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          # post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()

    return render_template('user/profile.html',
                           title='User',
                           user=user,
                           followers=followers,
                           following=following,
                           form=form,
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
        return redirect(url_for('user.profile', username=current_user.username))
    form.username.data = current_user.username
    form.bio.data = current_user.bio

    return render_template('user/edit_profile.html',
                           title='Edit Profile',
                           form=form)


@user.route('/discover/')
def discover():
    users = User.query.all()

    return render_template('user/discover.html',
                           title='Discover',
                           users=users)
