from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignupForm(FlaskForm):
    name = StringField(
        "Full name",
        validators=[DataRequired(message="Enter your name."), Length(min=2, max=120)],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Enter your email."), Email(message="Enter a valid email address."), Length(max=255)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Enter a password."), Length(min=8, message="Use at least 8 characters.")],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(message="Confirm your password."), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(message="Enter your email."), Email(message="Enter a valid email address.")],
    )
    password = PasswordField("Password", validators=[DataRequired(message="Enter your password.")])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")
