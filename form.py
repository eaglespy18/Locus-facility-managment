from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignUpForm(FlaskForm):
	name = StringField('Name:', validators=[DataRequired()])

	email = StringField('Email:', validators=[DataRequired(), Email(message=u'Invalid email address.')])

	phoneNum = StringField('Phone Number:', validators=[DataRequired(), Length(min=11, max=11)])

	username = StringField('Username:', validators=[DataRequired()])

	password = PasswordField('Password:', validators=[DataRequired(), Length(min=8)])

	confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])

	password = PasswordField('Password:', validators=[DataRequired()])

	submit = SubmitField('Login')


class AdminForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])

	password = PasswordField('Password', validators=[DataRequired()])

	submit = SubmitField('Login')

class BookForm(FlaskForm):
	date = DateField('Date', validators=[DataRequired()], format=('%d/%m/%y'), render_kw={"placeholder": "dd/mm/yy"})

	submit = SubmitField('Book')
