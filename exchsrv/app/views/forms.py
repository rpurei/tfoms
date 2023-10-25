#!python
#cython: language_level=3, always_allow_keywords=True
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.fields import EmailField


class LoginForm(FlaskForm):
    login = StringField('Имя для входа', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')


class RegisterForm(FlaskForm):
    login = StringField('Имя для входа', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('e-mail', validators=[DataRequired(), Email("Введите корректный адрес электронной почты")])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Подтвердите пароль', validators=[DataRequired()])
