from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import InputRequired,Length,Email,EqualTo,DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email()])
    password = StringField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class PoemForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Poem Content', validators=[DataRequired()])
    public = BooleanField('Make Public')
    submit = SubmitField('Submit Poem')
