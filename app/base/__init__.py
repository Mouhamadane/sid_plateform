from flask import Blueprint


blueprint = Blueprint(
    'admin_views',
    __name__,
    url_prefix='/admin',
    template_folder='templates',
    static_folder='static'
)