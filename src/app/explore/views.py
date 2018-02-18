import sys
from datetime import datetime
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
from app.explore import explore
from app.explore.forms import (
    CommentForm,
    UploadForm
)
from app.models import (
    Post,
    Comment,
)

@explore.route('/explore', methods=['GET', 'POST'])
def explore():
    current_user.last_user_notification_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(Post.likes) \
            .group_by(Post.id) \
            .order_by(db.func.count(Post.likes).desc()) \
            .order_by(Post.timestamp.desc()) \
            .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    print(posts, sys.stdout)
    next_url = url_for('explore.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('explore/explore.html',
                           title='Explore',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


# @explore.route('/details/<id>')
# @login_required
# def details(id):
#     post = Post.query.filter_by(id=id).first_or_404()
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(body=form.body.data,
#                           post=post,
#                           author=current_user._get_current_object())
#         db.session.add(comment)
#         db.session.commit()
#         flash('Your comment has been published.')
#         return redirect(url_for('posts.index'))

#     return render_template('explore/details.html',
#                            title='Details',
#                            form=form,
#                            post=post)
