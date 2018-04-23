import config
from flask import (
    Flask,
    render_template,
    request,
    current_app)
from app.extensions import (
    bcrypt,
    csrf_protect,
    db,
    login,
    migrate,
    moment,
    images,
    patch_request_class,
    configure_uploads,
    s3
)
from app.main import main as main_bp
from app.posts import posts as posts_bp
from app.users import users as users_bp
from app.api import api as api_bp
from app.admin import admin as admin_bp
from app.account import account as account_bp


def create_app(config_class):
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
    s3.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(account_bp, url_prefix='/account')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    return None


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.html'.format(error_code)), error_code
    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
