import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE = None
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'key'
    COMPANY_EMAIL = 'videovault.company48'
    SQLALCHEMY_DATABASE_URI = os.environ['AWS_RDS_URL']
    POSTS_PER_PAGE = 5  # How many items to display per page (for pagination)


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False

