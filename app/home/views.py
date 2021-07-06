import builtins
from operator import ne
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user, login_user

from app import db
from app.home import blueprint
from app.base.models import Permission, Reply, Role, User, Memory, Threads
from .forms import ChangePasswordForm, NewReply, NewThread


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                if user.role.role_name == 'Administrator':
                    login_user(user)
                    return redirect(url_for('admin_views.index'))
                else:
                    login_user(user)
                    return redirect(url_for('user_views.home_user'))
            else:
                flash('Mot de pass incorrect !', category='error')
        else:
            flash('Cet utilisateur n\'existe pas !', category='error')

    return render_template('user/login.html', user=current_user, users=User.query.all())


@blueprint.route('/user-home')
@login_required
def home_user():
    return render_template('user/index.html', user=current_user)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_views.index'))


@blueprint.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        password_conf = request.form.get('password2')
        role = Role.query.filter_by(permissions=Permission.GENERAL).first()
        user_testing = User.query.filter_by(email=email).first()

        if user_testing:
            flash('Cet adresse email existe déjà !', category='error')
        elif password != password_conf:
            flash('Mots de pass non identiques !', category='error')
        else:  # data are ok
            user_add = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                role=role
            )
            db.session.add(user_add)
            db.session.commit()
            return redirect(url_for('main_views.index'))

    return render_template('user/register.html')


@blueprint.route('/add-memory', methods=['GET', 'POST'])
@login_required
def add_memory():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        memory_link = request.form.get('link')

        memory = Memory(title=title, user=current_user.full_name(), year=year, memory_link=memory_link)
        db.session.add(memory)
        db.session.commit()
        flash('Votre mémoire a été ajouté avec succès !', category='success')

    return render_template('user/add_memory.html', user=current_user)


@blueprint.route('/list-memory', methods=['GET'])
@login_required
def list_memories():
    memories = Memory.query.all()
    return render_template('user/list_memory.html', memories=memories, user=current_user)


@blueprint.route('/<int:user_id>/change-password', methods=['GET','POST'])
@login_required
def change_password_user(user_id):
    """ change password's user """
    
    form = ChangePasswordForm()
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        if user.verify_password(form.old_password.data) and form.new_password.data==form.new_password2.data:
            user.password_hash = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('Votre mot de pass a été changé avec succès !', category='success')
        else: 
            flash('Une erreur est survenue, réessayez  !', category='error')
            
    return render_template('user/reset_password.html', form=form, user=current_user)

@blueprint.route('/thread', methods=['GET','POST'])
@login_required
def thread():
    form = NewThread()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
        
            new_thread = Threads(title=title, description=description)
            db.session.add(new_thread)
            db.session.commit()
        
    threads= Threads.query.all()
    
    return render_template('user/thread.html', form=form, user=current_user, threads=threads)


@blueprint.route('/<int:thread_id>/thread', methods=['GET', 'POST'])
@login_required
def get_thread(thread_id):
    form = NewReply()
    thread = Threads.query.get(int(thread_id))
    if request.method == 'POST':
        if form.validate_on_submit():
            reply = Reply(user_id=current_user.id, message=form.message.data)
            thread.replies.append(reply)
            db.session.commit()
            return redirect(url_for('user_views.get_thread', thread_id=reply.thread_id))
        
        
    replies = Reply.query.filter_by(thread_id=thread_id).all()
    
    return render_template('user/focus_thread.html', thread=thread, user=current_user, replies=replies, form=form)

    
