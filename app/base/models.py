from enum import unique
from operator import truediv
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import BadSignature, SignatureExpired
from sqlalchemy.orm import backref, lazyload
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app import db, login_manager



class Permission():
    GENERAL = 0x01
    ADMINISTER = 0xff

class Memory(db.Model):
    __tablename__ = 'memories'
    extend_existing=True
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200))
    year        = db.Column(db.String(10))
    memory_link = db.Column(db.String(200), unique=True)
    user        = db.Column(db.String(200))
    
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(65), unique=True)
    role_index = db.Column(db.String(65))
    default = db.Column(db.Boolean, default=True, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.GENERAL, 'main', True),
            'Administrator': (Permission.ADMINISTER, 'admin', False)
        }
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
                role.permissions = roles[r][0]
                role.role_index = roles[r][1]
                role.default = roles[r][2]
                db.session.add(role)
        db.session.commit()
    
    def __repr__(self):
        return "< Role '%s'>" % self.role_name
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(150))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    replies = db.relationship('Reply', backref='user', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions = Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
          

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
    
    def admin(self):
        return self.can(Permission.ADMINISTER)
    
    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_fake(count=10, **kwargs):
        from sqlalchemy.exc import IntegrityError
        from faker import Faker
        from random import seed, choice
        
        fake = Faker()
        roles = Role.query.all()
        
        seed()
        for i in range(count):
            user = User(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                email = fake.email(),
                password = 'passer',
                confirmed = True,
                role = choice(roles),
                **kwargs
            )
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class Threads(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(120))   
    description = db.Column(db.String(200))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship('Reply', backref='thread', lazy='dynamic')
    
    def last_post_reply(self):
        last_reply = Reply.query.filter_by(thread_id=self.id).order_by(Reply.created_at.desc()).first()
        if last_reply:
            return last_reply.created_at
        return self.create_at
    
    
class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
      
 
class EditableHTML(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    editor_name = db.Column(db.String(100), unique=True)
    value = db.Column(db.Text)

    @staticmethod
    def get_editable_html(editor_name):
        editable_html_obj = EditableHTML.query.filter_by(
            editor_name=editor_name).first()

        if editable_html_obj is None:
            editable_html_obj = EditableHTML(editor_name=editor_name, value='')
        return editable_html_obj
    
    
class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser      
    
@login_manager.user_loader
def loader_user(key):
    return User.query.get(int(key))