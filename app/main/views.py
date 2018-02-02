from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app)
from app.extensions import db, images
from app.main import main
from app.main.forms import UploadForm
from app.models import Post
from werkzeug.utils import secure_filename


@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['photo']
        filename = secure_filename(file.filename)
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


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('main/index.html',
                           title='Explore')
