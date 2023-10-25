#!python
#cython: language_level=3, always_allow_keywords=True
from app.models.db import db_exchsrv
from app.config import (DEFAULT_ADMIN_LOGIN, DEFAULT_ADMIN_PASSWORD,
                        DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_NAME)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from flask_login import UserMixin


class User(UserMixin, db_exchsrv.Model):
    __bind_key__ = 'exchsrv'
    __tablename__ = 'users'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    login = db_exchsrv.Column(db_exchsrv.String(128), unique=True)
    name = db_exchsrv.Column(db_exchsrv.String(128))
    email = db_exchsrv.Column(db_exchsrv.String(128))
    password = db_exchsrv.Column(db_exchsrv.String(128))
    active = db_exchsrv.Column(db_exchsrv.Boolean, default=False)

    def __init__(self, login, name, email, active=1):
        self.login = login
        self.name = name
        self.email = email
        self.active = active

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User {}>'.format(self.login)


@event.listens_for(User.__table__, 'after_create')
def create_admin(*args, **kwargs):
    admin_add = User(login=DEFAULT_ADMIN_LOGIN,
                     email=DEFAULT_ADMIN_EMAIL,
                     name=DEFAULT_ADMIN_NAME,
                     active=True)
    admin_add.set_password(DEFAULT_ADMIN_PASSWORD)
    db_exchsrv.session.add(admin_add)
    db_exchsrv.session.commit()


class UserRole(db_exchsrv.Model):
    __bind_key__ = 'exchsrv'
    __tablename__ = 'user_roles'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    user_id = db_exchsrv.Column(db_exchsrv.Integer,
                                db_exchsrv.ForeignKey('users.id'))
    role_id = db_exchsrv.Column(db_exchsrv.Integer,
                                db_exchsrv.ForeignKey('roles.id'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    def serialize(self):
        return {
                'id': self.id,
                'user_id': self.user_id,
                'role_id': self.role_id
                }


class Role(db_exchsrv.Model):
    __bind_key__ = 'exchsrv'
    __tablename__ = 'roles'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    name = db_exchsrv.Column(db_exchsrv.String(64))

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {'id': self.id, 'name': self.name}


class Permission(db_exchsrv.Model):
    __bind_key__ = 'exchsrv'
    __tablename__ = 'permissions'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    name = db_exchsrv.Column(db_exchsrv.String(64))

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name
               }


class RolePermission(db_exchsrv.Model):
    __bind_key__ = 'exchsrv'
    __tablename__ = 'role_permissions'
    id = db_exchsrv.Column(db_exchsrv.Integer, primary_key=True)
    role_id = db_exchsrv.Column(db_exchsrv.Integer,
                                db_exchsrv.ForeignKey('roles.id'))
    permission_id = db_exchsrv.Column(db_exchsrv.Integer,
                                      db_exchsrv.ForeignKey('permissions.id'))

    def __init__(self, role_id, permission_id):
        self.role_id = role_id
        self.permission_id = permission_id

    def serialize(self):
        return {
                'id': self.id,
                'role_id': self.role_id,
                'permission_id': self.permission_id
                }


@event.listens_for(Role.__table__, 'after_create')
def create_admin_roles(*args, **kwargs):
    role_add = Role(name='admin')
    db_exchsrv.session.add(role_add)
    db_exchsrv.session.commit()


@event.listens_for(UserRole.__table__, 'after_create')
def add_admin_role(*args, **kwargs):
    user_role_add = UserRole(user_id=1, role_id=1)
    db_exchsrv.session.add(user_role_add)
    db_exchsrv.session.commit()


@event.listens_for(Permission.__table__, 'after_create')
def create_admin_role_permissions(*args, **kwargs):
    role_perm_add = Permission(name='admin:read')
    db_exchsrv.session.add(role_perm_add)
    role_perm_add = Permission(name='admin:insert')
    db_exchsrv.session.add(role_perm_add)
    role_perm_add = Permission(name='admin:update')
    db_exchsrv.session.add(role_perm_add)
    role_perm_add = Permission(name='admin:delete')
    db_exchsrv.session.add(role_perm_add)
    db_exchsrv.session.commit()


@event.listens_for(RolePermission.__table__, 'after_create')
def add_admin_role_permissions(*args, **kwargs):
    role_perm_add = RolePermission(role_id=1, permission_id=1)
    db_exchsrv.session.add(role_perm_add)
    role_perm_add = RolePermission(role_id=1, permission_id=2)
    db_exchsrv.session.add(role_perm_add)
    role_perm_add = RolePermission(role_id=1, permission_id=3)
    db_exchsrv.session.add(role_perm_add)
    role_perm_add = RolePermission(role_id=1, permission_id=4)
    db_exchsrv.session.add(role_perm_add)
    db_exchsrv.session.commit()
