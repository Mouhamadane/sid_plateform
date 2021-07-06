import os
from importlib import import_module

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect

from config import config_dict

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
mail = Mail()
DB_NAME = 'database.db'
login_manager = LoginManager()
login_manager.login_view = 'user_views.login'
# csrf = CSRFProtect()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


def database_init(app):
    if not os.path.exists('app/'+ DB_NAME):
        db.create_all(app=app)
        print('DataBase create successfully !')



def register_blueprints(app):
    for module_name in ('base','home','main'):
        module = import_module('app.{}.views'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app(config):
    app = Flask(__name__)
    config_name = 'Production'
    
    app.config.from_object(config_dict[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    config_dict[config_name].init_app(app)

    

    register_blueprints(app)
    register_extensions(app)
    database_init(app)

    return app

