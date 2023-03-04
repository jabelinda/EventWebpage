from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    firstname = StringField('Name', validators=[DataRequired(), Length(min=2, max=24)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=24)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=24)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=9, max=24)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    about = TextAreaField('Describe your self', validators=[DataRequired(), Length(min=2, max=200)])
    sex = SelectField('Female or Male', choices=['Female' 'Male'], validate_choice=True, validators=[DataRequired()])
    submit = SubmitField('Sing Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
