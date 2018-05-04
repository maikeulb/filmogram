import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'S3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres:P@ssw0rd!@172.17.0.2/filmogram'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@email.com'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'P@ssw0rd!'

    DEMO_EMAIL = 'demo@email.com'
    DEMO_PASSWORD = 'P@ssw0rd!'

    DEMO_ADMIN_EMAIL = 'demo_admin@mail.com'
    DEMO_ADMIN_PASSWORD = 'P@ssw0rd!'

    UPLOADS_DEFAULT_DEST = basedir + '/app/static/uploads/'
    UPLOADS_DEFAULT_URL = os.environ.get(
        'UPLOADS_DEFAULT_URL') or 'http://localhost:5000/static/uploads/'
    POSTS_PER_PAGE = 4

    AWS_ACCESS_KEY_ID = os.environ.get("S3_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")
    FLASKS3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    FLASKS3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com/'
    FLASKS3_BUCKET_DOMAIN = 'https://{}.nyc3.digitaloceanspaces.com/'.format(
        FLASKS3_BUCKET_NAME)
    FLASKS3_REGION = 'nyc3'

    REDIS_HOST = os.getenv('REDIS_HOST', '172.17.0.3')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)

    DEVELOPMENT = False
    TESTING = False
    PRODUCTION = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    DEBUG_TB_ENABLED = True


class ProductionConfig(Config):
    PRODUCTION = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
