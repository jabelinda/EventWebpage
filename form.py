from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    firstname = StringField('Namn',
                            validators=[DataRequired(), Length(min=2, max=24)])
    lastname = StringField('Efternamn',
                           validators=[DataRequired(), Length(min=2, max=24)])
    username = StringField('Användarnamn',
                           validators=[DataRequired(), Length(min=2, max=24)])
    password = PasswordField('Lösenord',
                             validators=[DataRequired(), Length(min=9, max=24)])
    confirm_password = PasswordField('Repetera lösenord',
                                     validators=[DataRequired(), EqualTo('password')])
    image = StringField('Bild')
    about = TextAreaField('Kort om dig')

    submit = SubmitField('Sing Up')


class LoginForm(FlaskForm):
    username = StringField('Användarnamn',
                           validators=[DataRequired()])
    password = PasswordField('Lösenord',
                             validators=[DataRequired()])
    remember = BooleanField('Kom ihåg mig')
    submit = SubmitField('Login')
