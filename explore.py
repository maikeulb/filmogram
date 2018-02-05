
@main.route('/explore', methods=['GET', 'POST'])
def explore():
    current_user.last_user_notification_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(Post.likes) \
            .group_by(Post.id) \
            .order_by(db.func.count(Post.likes).desc()) \
            .order_by(db.func.count(Post.likes).desc()) \
            .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.favorites', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.favorites', page=posts.prev_num) \
        if posts.has_prev else None
    print(posts, sys.stdout)
    print('hi', sys.stdout)
    return render_template('main/explore.html',
                           title='Explore',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)


<script>
$('.grid').masonry({
  itemSelector: '.grid-item',
  columnWidth: 200,
  stagger: 30
  });
</script>

