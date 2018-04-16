import sys
from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from app.extensions import db, images
from app.posts import posts
from app.posts.forms import (
    CommentForm,
    UploadForm
)
from app.models import (
    Post,
    Comment,
)


@posts.route('/feed')
@login_required
def index():
    form = CommentForm()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('posts.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.index', page=posts.prev_num) \
        if posts.has_prev else None
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/index.html',
                           title='Followed Posts',
                           posts=posts.items,
                           form=form,
                           next_url=next_url,
                           prev_url=prev_url)


@posts.route('/favorites')
def favorites():
    form = CommentForm()
    page = request.args.get('page', 1, type=int)
    posts = current_user.liked_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('posts.favorites', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('posts.favorites', page=posts.prev_num) \
        if posts.has_prev else None
    print(posts.items, file=sys.stdout)
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()

    return render_template('posts/index.html',
                           title='Favorites',
                           posts=posts.items,
                           form=form,
                           next_url=next_url,
                           prev_url=prev_url)


@posts.route('/post', methods=['GET', 'POST'])
@login_required
def post():
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
        return redirect(url_for('posts.index'))

    return render_template('posts/post.html',
                           title='Post',
                           form=form)


@posts.route('/details/<id>')
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
        return redirect(url_for('posts.index'))

    return render_template('posts/details.html',
                           title='Details',
                           form=form,
                           post=post)
