from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from app import images


class UploadForm(FlaskForm):
    photo_description = StringField('Caption', validators=[DataRequired()],
                                    widget=TextArea())
    photo = FileField('Photo Upload', validators=[FileAllowed(images, 'Image Only!'),
                                                  FileRequired('Choose a file!')])
    submit = SubmitField('Upload')


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
