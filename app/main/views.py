from flask import Blueprint, render_template
from flask_login import current_user

from app.base.models import EditableHTML
from app.main import blueprint


@blueprint.route('/')
def index():
    return render_template('main/index.html', user=current_user)


@blueprint.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
