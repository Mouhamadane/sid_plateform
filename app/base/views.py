from flask import redirect, url_for, request, render_template, flash
from flask_login import current_user, login_required

from app import db
from app.base import blueprint
from app.base.models import User, Role, Permission
from app.decorators import admin_required



@blueprint.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html', user=current_user)
    
@blueprint.route('/add-user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name  = request.form.get('lastName')
        email      = request.form.get('email')
        password   = request.form.get('password')
        confirmed   = request.form.get('password2')
        user_query = User.query.filter_by(email=email).first()
        role = Role.query.filter_by(permissions=Permission.ADMINISTER).first()
        if user_query:
            flash('Cet adresse email existe déja !', category='error')
        elif password != confirmed:
            flash('Passwords must match.', category='error')
        else:
            user = User(
                email      = email,
                first_name = first_name,
                last_name  = last_name,
                role       = role,
                password   = password
            )
            db.session.add(user)
            db.session.commit()
            flash(' Admin {} a été ajouté avec succès !'.format(user.full_name()),
                  category='success')
    return render_template('admin/adduser.html', user=current_user)

@blueprint.route('/<int:user_id>/change-email', methods=['GET','POST'])
@login_required
@admin_required
def change_mail_user(user_id):
    """ Change mail user """
    if request.method == 'POST':
        user = User.query.filter_by(id=user_id).first()
        if not user:
            flash('Une erreur est survenue sur la requête !', category='error')
        email = request.form.get('email')
        user.email = email
        db.session.add(user)
        db.session.commit()
        flash('Votre adresse email a été changé avec succès !', category='success')
        
    return render_template('admin/reset_email.html', user=current_user)
        
        
    


@blueprint.route('/users')
@login_required
@admin_required
def registed_users():
    """ All users registed """
    roles = Role.query.all()
    users = User.query.all()
    return render_template('admin/registred_users.html', user=current_user, users=users, roles=roles)


@blueprint.route('/user<int:user_id>/_delete')
@login_required
@admin_required
def delete_user(user_id):
    """ Delete a user's account. """
    if current_user.id == user_id:
        flash('Vous ne pouvez pas supprimer votre compte !', category='error')
    else:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        flash('{} a été supprimé avec succès'.format(user.full_name()), category='success')
        
    return redirect(url_for('admin_views.registed_users'))

@blueprint.route('/memoires', methods=['GET'])
@login_required
@admin_required
def get_memory():
    all_memories = User.query.all()
    
    return ' Test'





