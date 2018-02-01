from datetime import datetime
from flask import (
    render_template,
    flash, redirect,
    url_for,
    request,
    current_app)
from flask_login import current_user, login_required
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from app.extensions import login, db
from app.main import main
from app.main.forms import UploadForm, photos
from werkzeug import secure_filename


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            name = secure_filename(filename.filename)
            photos.save(filename, name=name + '.')
        success = True
    else:
        success = False
    return render_template('main/index.html', 
                           form=form, 
                           success=success)
