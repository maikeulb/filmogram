from flask_uploads import (
    UploadSet, 
    configure_uploads, 
    IMAGES,
    patch_request_class
)
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

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('About me', validators=[Length(min=0, max=140)])
    profile_img = FileField('Photo Upload', validators=[FileAllowed(images, 'Image Only!'), FileRequired('Choose a file!')])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
