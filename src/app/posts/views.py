import sys
import time
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
from app import spaces, redis


@posts.before_request
@login_required
def require_login():
    pass


@posts.route('/')
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


@posts.route('/upload', methods=['GET', 'POST'])
def post():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['photo']
        url = spaces.upload_file(file=file)
        post = Post(caption=form.photo_description.data,
                    photo_url=url,
                    author=current_user)
        db.session.add(post)
        db.session.commit()

        post_id = post.id
        user_id = current_user.id
        post_id_key = redis.POST_KEY_FORMAT.format(post_id)
        post_id_feed_key = redis.USER_FEED_KEY_FORMAT.format(user_id)
        post_id_user_key = redis.USER_POSTS_KEY_FORMAT.format(user_id)
        unix_time = int(time.time())

        followers = []
        for follower in current_user.get_my_following():
            followers.append(follower.id)

        with redis.r.pipeline() as pipe:
            pipe.multi()

            pipe.hmset(post_id_key,
                       {redis.POST_USERID_KEY: user_id,
                        redis.POST_UNIXTIME_KEY: unix_time,
                        redis.POST_BODY_KEY: post})

            pipe.lpush(post_id_feed_key, post_id)
            pipe.lpush(post_id_user_key, post_id)

            for follower in followers:
                post_id_follower_key = redis.USER_FEED_KEY_FORMAT.format(
                    follower)
                pipe.lpush(post_id_follower_key, post_id)

            pipe.lpush(redis.GENERAL_FEED_KEY, post_id)
            pipe.ltrim(redis.GENERAL_FEED_KEY, 0,
                       redis.GENERAL_FEED_MAX_POST_CNT - 1)

            pipe.execute()

        flash('Your post is now live!')
        return redirect(url_for('posts.index'))

    return render_template('posts/post.html',
                           title='Post',
                           form=form)


@posts.route('/details/<id>')
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
