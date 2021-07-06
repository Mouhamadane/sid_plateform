import os
import sys


PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    print('Importing environnement from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

class Config():
    APP_NAME = os.environ.get('APP_NAME', 'SID_PLATEFORME')
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('Should not see in production')
    SQLALCHEMEY_COMMIT_ON_TEARDOWN = True

    # Email configuration 
    MAIL_SERVER        = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT          = os.environ.get('MAIL_PORT', 587)
    MAIL_USE_TLS       = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL       = os.environ.get('MAIL_USE_SSL', False)
    MAIL_USERNAME      = os.environ.get('MAIL_USERNAME', 'damanyelegrand@gmail.com')
    MAIL_PASSWORD      = os.environ.get('MAIL_PASSWORD', 'dane158dane.')
    MAIL_DEFAUT_SENDER = os.environ.get('MAIL_DEFAUT_SENDER', True)

    # Admin account
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'passer')
    ADMIN_EMAIL     = os.environ.get('ADMIN_MAIL', 'admin@admin.com')
    EMAIL_SENDER   = '{app_name} Admin <{email}>'.format(
        app_name=APP_NAME, email=MAIL_USERNAME)
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG        = True
    ASSETS_DEBUG = True
    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE . \
            YOU SHOULD NOT SEE THIS IN PROD')


class ProductionConfig(Config):
    DEBUG        = False
    ASSETS_DEBUG = False
    
    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True') 

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY', 'SECRET_KEY IS NOT SET')
 

config_dict = {
    'Production': ProductionConfig,
    'Default'   : DevelopmentConfig
}

