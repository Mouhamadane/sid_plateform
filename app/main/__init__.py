from flask import Blueprint

blueprint = Blueprint(
    'main_views',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)
