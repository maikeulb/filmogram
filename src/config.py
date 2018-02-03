import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path)


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'S3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
      'postgresql://postgres:P@ssw0rd!@172.17.0.3/filmogram'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADS_DEFAULT_DEST = basedir + '/app/static/uploads/'
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/uploads/'
    POSTS_PER_PAGE = 4
 
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
    DATABASE_URI = ''
    PRODUCTION = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4  
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False  
