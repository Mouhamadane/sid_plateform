import os

from flask_migrate import Migrate
from flask_script import Manager, Shell

from config import Config
from app import create_app, db
from app.base.models import Role, User, Permission

config = (os.getenv('FLASK_CONFIG') or 'Production')
app = create_app(config)
migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(db=db, User=User, app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def recreate_db():
    """
        Recreates a local database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='test',
    dest='number_users')
def add_fake_date(number_users):
    """ Adds fake data to the database """
    
    User.generate_fake(count=number_users)


def setup_dev():
    setup_general()
    
@manager.command
def setup_general():
    """ 
        This function is used to initialise the first admin user.
    """
    Role.insert_roles()
    admin_query = Role.query.filter_by(role_name='Administrator').first()
    if admin_query is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                email      = Config.ADMIN_EMAIL,
                first_name = "Zeynab",
                last_name  = "Hamout",
                password   = Config.ADMIN_PASSWORD,
                confirmed  = True
                )
            db.session.add(user)
            db.session.commit()
            print(' Added admin {}'.format(user.full_name()))

if __name__ == '__main__':
    manager.run()

