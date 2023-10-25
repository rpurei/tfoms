#!python
#cython: language_level=3, always_allow_keywords=True
from app.models.db import db_exchsrv
from app.auth.model import User
from app.config import LOCAL_DATABASE_URI, APP_VER

from flask_login import LoginManager
from flask import render_template, redirect, flash, url_for, request, current_app, Blueprint
from flask_login import logout_user, current_user, login_user, login_required
from .forms import LoginForm, RegisterForm
from sqlalchemy import create_engine, text

login_manager = LoginManager()
users_handler = Blueprint('users', __name__)


@login_required
@users_handler.route('/users', methods=['GET'])
def users_show():
    result_list = []
    result_header = ['ID', 'Логин', 'Имя', 'e-mail', 'Включен']
    login = ''
    if current_user.is_authenticated:
        login = current_user.name
    try:
        database_engine = create_engine(LOCAL_DATABASE_URI, echo=False)
        with database_engine.connect() as conn:
            result = conn.execute(text(f'SELECT id,login,name,email,active FROM users'))
            for row in result:
                result_list.append((row[0], row[1], row[2], row[3], row[4]))
            return render_template('users.html', login=login, result_data=result_list, result_header=result_header)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@users_handler.route('/user/<path:userid>/edit', methods=['GET'])
def user_edit(userid):
    result_list = []
    login = ''
    if current_user.is_authenticated:
        login = current_user.name
    try:
        database_engine = create_engine(LOCAL_DATABASE_URI, echo=True)
        with database_engine.connect() as conn:
            result = conn.execute(text(f'SELECT id,login,name,email,active FROM users WHERE id=:user_id'),
                                  user_id=userid)
            for row in result:
                active = '<div><i class="bi bi-check-circle" style="color: green;"></i></div>' if row[4] == 1 else '<div><i class="bi bi-x-circle" style="color: red;></i></div>'
                result_list.append((row[0], row[1], row[2], row[3], active, row[4]))
            return render_template('user_edit.html', login=login, result_data=result_list)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@users_handler.route('/user/<path:userid>/save', methods=['POST'])
def user_save(userid):
    try:
        user = User.query.filter_by(id=userid).first()
        name = request.form.get('name')
        email = request.form.get('email')
        active = request.form.get('active')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        user.name = name if user.name != name else user.name
        user.email = email if user.email != email else user.email
        user.active = int(active) if user.active != active else user.active
        if password != '********':
            if password != password_confirm:
                flash('Пароль и подтверждение не совпадают', 'danger')
                return redirect(url_for('users.user_edit', userid=userid))
            else:
                user.set_password(password)
        elif password == '':
            flash('Пароль не может быть пустым', 'danger')
            return redirect(url_for('users.user_edit', userid=userid))
        db_exchsrv.session.add(user)
        db_exchsrv.session.commit()
        flash('Данные пользователя обновлены', 'success')
        return redirect(url_for('users.users_show'))
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')


@login_required
@users_handler.route('/user/register', methods=['GET', 'POST'])
def register_show():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User.query.filter_by(login=register_form.login.data).first()
        if user:
            flash('Пользователь с таким логином уже существует, выберите другой логин', 'warning')
        else:
            if register_form.password.data == register_form.password_repeat.data:
                user = User(register_form.login.data, register_form.name.data, register_form.email.data)
                user.set_password(register_form.password.data)
                db_exchsrv.session.add(user)
                db_exchsrv.session.commit()
                flash(f'Пользователь {user.login} зарегистрирован', 'success')
                return redirect(url_for('users.users_show'))
            else:
                flash('Введенные пароли не совпадают', 'warning')
    return render_template('register.html', register_form=register_form)


@users_handler.route('/user/login', methods=['GET', 'POST'])
def auth_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(login=login_form.login.data).first()
        if user and user.check_password(password=login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('transactions.index_show'))
        flash('Неверное имя пользователя/пароль', 'danger')
        return redirect(url_for('users.auth_login'))
    return render_template('login.html', login_form=login_form, app_ver=APP_VER)


@users_handler.route('/user/logout')
def auth_logout():
    logout_user()
    return redirect(url_for('transactions.index_show'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash(f'Авторизуйтесь для доступа к странице', 'warning')
    return redirect(url_for('auth.login'))
