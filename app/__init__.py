import config
import os

from flask import (
    Flask, 
    render_template, 
    request, 
    current_app)
from app import commands, models
from app.account import account as account_bp
from app.extensions import (
    bcrypt, 
    csrf_protect, 
    db,
    login, 
    migrate, 
    moment,
    images,
    configure_uploads,
    patch_request_class
)
from app.main import main as main_bp
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES

Config = eval(os.environ['FLASK_APP_CONFIG'])


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_blueprints(app)
    register_extensions(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    configure_uploads(app, images)
    patch_request_class(app)
    return None


def register_blueprints(app):
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(main_bp)
    return None

def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def register_shellcontext(app):
    def shell_context():
        return {
            'db': db,
            'User': models.User}
    app.shell_context_processor(shell_context)
