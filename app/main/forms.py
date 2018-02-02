from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import User
from app import images


class UploadForm(FlaskForm):
    photo_description = StringField('Caption', validators=[DataRequired()])
    photo = FileField('Photo Upload', validators=[FileAllowed(images, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Upload')
